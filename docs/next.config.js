const withMDX = require("@next/mdx")({
  extensions: /\.mdx?$/,
})

module.exports = withMDX({
  pageExtensions: ['js', 'jsx', 'mdx']

})
