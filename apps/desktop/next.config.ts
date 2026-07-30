import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  output: 'export',
  distDir: 'out',
  images: { unoptimized: true },
  reactStrictMode: true,
  transpilePackages: ['@scilab-studio/widgets', '@scilab-studio/core', '@scilab-studio/runtime', '@scilab-studio/workspace'],
};

export default nextConfig;
