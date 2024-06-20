module.exports = {
  singleQuote: true,
  trailingComma: 'all',
  arrowParens: 'avoid',
  proseWrap: 'preserve',
  quoteProps: 'as-needed',
  bracketSameLine: false,
  bracketSpacing: true,
  tabWidth: 2,
  semi: false,
  plugins: ['@trivago/prettier-plugin-sort-imports'],
  importOrderParserPlugins: ['typescript', 'jsx', 'decorators'],
  // Sort-imports
  importOrder: [
    '^react(.*)',
    'next/(.*)',
    '<THIRD_PARTY_MODULES>',
    '@/(.*)',
    '^[./]',
  ],
  importOrderSeparation: true,
  importOrderSortSpecifiers: true,
}
