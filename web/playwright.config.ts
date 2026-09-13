import { defineConfig } from '@playwright/test';
export default defineConfig({
  testDir:'./tests',timeout:60000,workers:1,
  use:{baseURL:process.env.WALKTHROUGH_URL || 'http://127.0.0.1:5173',viewport:{width:1400,height:900},
    launchOptions:{executablePath:'/usr/bin/google-chrome',args:['--use-angle=swiftshader','--enable-unsafe-swiftshader']},
  },
});
