#!/usr/bin/env node
'use strict';

const { spawnSync } = require('node:child_process');
const path = require('node:path');

const script = path.resolve(__dirname, '..', 'scripts', 'w_model_install.py');
const result = spawnSync('python3', [script, ...process.argv.slice(2)], { stdio: 'inherit' });

if (result.error) {
  console.error(`w-model-install: ${result.error.message}`);
  process.exit(2);
}
process.exit(result.status ?? 2);
