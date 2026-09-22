#!/usr/bin/env node
// Read-only smoke check. Resolve toolchain from an existing project, no installs.
const fs = require('node:fs')
const path = require('node:path')
const assert = require('node:assert/strict')
const { createRequire } = require('node:module')
const { pathToFileURL } = require('node:url')

async function main() {
  const args = process.argv.slice(2)
  if (args.length !== 2 || args[0] !== '--project') {
    throw new Error('Usage: node scripts/check-assets.cjs --project <existing Vue 3 / Tailwind 3 project>')
  }
  const project = path.resolve(args[1])
  assert.ok(fs.existsSync(path.join(project, 'package.json')), 'Project package.json not found')
  const projectRequire = createRequire(path.join(project, 'package.json'))
  const root = path.resolve(__dirname, '..')
  const assets = path.join(root, 'assets')
  const compiler = projectRequire('@vue/compiler-sfc')
  const ts = projectRequire('typescript')
  const postcss = projectRequire('postcss')
  const tailwind = projectRequire('tailwindcss')
  const autoprefixer = projectRequire('autoprefixer')
  assert.match(projectRequire('tailwindcss/package.json').version, /^3\./, 'These assets target Tailwind 3')
  const preset = require(path.join(assets, 'tailwind.preset.cjs'))
  assert.equal(preset.theme.extend.colors.primary[900], '#1a1f36')
  assert.equal(preset.theme.extend.colors.accent[500], '#3b82f6')
  assert.ok(preset.theme.extend.fontFamily.sans.includes('system-ui'))

  const walk = dir => fs.readdirSync(dir, { withFileTypes: true }).flatMap(entry => {
    const file = path.join(dir, entry.name)
    return entry.isDirectory() ? walk(file) : [file]
  })
  const files = walk(root)
  const markdown = files.filter(file => file.endsWith('.md'))
  let linkCount = 0
  for (const file of markdown) {
    const source = fs.readFileSync(file, 'utf8')
    for (const match of source.matchAll(/\[[^\]]*\]\(([^)]+)\)/g)) {
      const href = match[1].replace(/^<|>$/g, '')
      if (/^(?:https?:|#)/.test(href)) continue
      const target = path.resolve(path.dirname(file), decodeURIComponent(href.split('#')[0]))
      assert.ok(fs.existsSync(target), `Broken reference: ${file} -> ${href}`)
      linkCount++
    }
  }

  const vueFiles = files.filter(file => file.endsWith('.vue'))
  const sources = []
  for (const file of vueFiles) {
    const source = fs.readFileSync(file, 'utf8')
    sources.push(source)
    const parsed = compiler.parse(source, { filename: file })
    assert.equal(parsed.errors.length, 0, `${file}: ${parsed.errors.join('\n')}`)
    const id = path.basename(file).replace(/\W/g, '_')
    const script = compiler.compileScript(parsed.descriptor, { id, inlineTemplate: true })
    const transpiled = ts.transpileModule(script.content, {
      compilerOptions: { target: ts.ScriptTarget.ES2020, module: ts.ModuleKind.ESNext },
      fileName: file + '.ts', reportDiagnostics: true,
    })
    const errors = (transpiled.diagnostics || []).filter(d => d.category === ts.DiagnosticCategory.Error)
    assert.equal(errors.length, 0, errors.map(d => ts.flattenDiagnosticMessageText(d.messageText, '\n')).join('\n'))
    // Confirm named icon exports exist in the target's installed icon package.
    const ast = ts.createSourceFile(file + '.ts', script.content, ts.ScriptTarget.Latest, true)
    for (const statement of ast.statements) {
      if (!ts.isImportDeclaration(statement)) continue
      const specifier = statement.moduleSpecifier.text
      if (specifier.startsWith('.')) {
        assert.ok(fs.existsSync(path.resolve(path.dirname(file), specifier)), `Unresolved local import: ${specifier}`)
      } else {
        projectRequire.resolve(specifier)
        if (specifier === 'lucide-vue-next') {
          const exports = projectRequire(specifier)
          const bindings = statement.importClause?.namedBindings
          if (bindings && ts.isNamedImports(bindings)) {
            for (const item of bindings.elements) assert.ok(exports[(item.propertyName || item.name).text], `Missing Lucide icon: ${item.name.text}`)
          }
        }
      }
    }
  }

  const cssFile = path.join(assets, 'admin-ui.css')
  const css = fs.readFileSync(cssFile, 'utf8')
  const componentClasses = Array.from(css.matchAll(/\.([a-zA-Z][\w-]*)/g), match => match[1]).join(' ')
  const result = await postcss([
    tailwind({ presets: [preset], content: [{ raw: sources.join('\n') + '\n' + componentClasses, extension: 'html' }] }),
    autoprefixer(),
  ]).process(css, { from: cssFile })
  assert.ok(!/@(?:apply|tailwind)\b/.test(result.css), 'Unprocessed Tailwind directive')
  for (const selector of ['.app-shell', '.feishu-table', '.feishu-input', '.btn-primary', '.admin-field', '.admin-dialog-card', '.bg-primary-900']) {
    assert.ok(result.css.includes(selector), `Missing generated selector: ${selector}`)
  }

  // Bundle both SFCs as an ES library, in memory, with the target's Vite toolchain.
  function esmEntry(name) {
    let directory = path.dirname(projectRequire.resolve(name))
    while (true) {
      const manifestPath = path.join(directory, 'package.json')
      if (fs.existsSync(manifestPath)) {
        const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf8'))
        if (manifest.name === name) {
          const entry = manifest.exports?.['.']?.import
          const relative = typeof entry === 'string' ? entry : entry?.default
          assert.ok(relative, `ES module entry not found for ${name}`)
          return pathToFileURL(path.resolve(directory, relative)).href
        }
      }
      const parent = path.dirname(directory)
      assert.notEqual(directory, parent, `Package root not found for ${name}`)
      directory = parent
    }
  }
  const { build } = await import(esmEntry('vite'))
  const vueModule = await import(esmEntry('@vitejs/plugin-vue'))
  const vue = vueModule.default
  const bundle = await build({
    configFile: false, envFile: false, root: assets, publicDir: false, logLevel: 'error',
    plugins: [vue()],
    build: {
      write: false, minify: false,
      lib: { entry: path.join(assets, 'AdminUiExample.vue'), formats: ['es'], fileName: 'admin-ui-example' },
      rollupOptions: { external: ['vue', 'lucide-vue-next'] },
    },
  })
  const outputs = (Array.isArray(bundle) ? bundle : [bundle]).flatMap(item => item.output || [])
  assert.ok(outputs.some(output => output.type === 'chunk' && output.isEntry), 'No entry chunk built')
  console.log(`PASS: ${linkCount} documentation links, ${vueFiles.length} Vue SFCs, icon exports, preset, CSS (${result.css.length} chars), in-memory Vite library build.`)
  console.log('Scope: compilation and resource checks; not full TypeScript, browser, or API validation. No project files written.')
}

main().catch(error => { console.error(error.stack || error.message); process.exitCode = 1 })
