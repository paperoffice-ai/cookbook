#!/usr/bin/env node
/** PaperOffice AI — Health Check (VISITOR, no token required) */
const response = await fetch("https://api.paperoffice.ai/latest/health");
const data = await response.json();
console.log(`Status: ${data.success}`);
console.log(`Message: ${data.message}`);
console.log(`Processing: ${data.processing_time}`);
