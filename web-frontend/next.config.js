/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,

  // Environment variables dostupné v browseru
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001',
  },

  // Image optimization
  images: {
    domains: [],  // Přidat Supabase CDN později
  },
}

module.exports = nextConfig
