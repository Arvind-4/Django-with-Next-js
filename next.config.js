/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  distDir: "../.next",
  generateBuildId: async () => {
    return 'static';
  }
}

module.exports = nextConfig
