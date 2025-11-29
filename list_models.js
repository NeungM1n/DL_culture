import { GoogleGenerativeAI } from "@google/generative-ai";
import fs from 'fs';
import path from 'path';

// Read .env manually
const envPath = path.resolve(process.cwd(), '.env');
let apiKey = '';

try {
    const envContent = fs.readFileSync(envPath, 'utf-8');
    const match = envContent.match(/VITE_API_KEY=(.*)/);
    if (match) {
        apiKey = match[1].trim();
        // Remove quotes if present
        if (apiKey.startsWith('"') && apiKey.endsWith('"')) {
            apiKey = apiKey.slice(1, -1);
        } else if (apiKey.startsWith("'") && apiKey.endsWith("'")) {
            apiKey = apiKey.slice(1, -1);
        }
    }
} catch (e) {
    console.error("Could not read .env file");
}

if (!apiKey) {
    console.error("API Key not found in .env");
    process.exit(1);
} else {
    // Mask key for safety in logs
    const maskedKey = apiKey.length > 8 ? `${apiKey.substring(0, 5)}...${apiKey.substring(apiKey.length - 3)}` : "SHORT_KEY";
    console.log(`API Key found: ${maskedKey} (Length: ${apiKey.length})`);
}

const genAI = new GoogleGenerativeAI(apiKey);

async function testModel(modelName) {
    console.log(`Testing ${modelName}...`);
    try {
        const model = genAI.getGenerativeModel({ model: modelName });
        const result = await model.generateContent("Hello");
        console.log(`SUCCESS: ${modelName} works!`);
        return true;
    } catch (error) {
        console.log(`FAILED: ${modelName} - ${error.message}`);
        return false;
    }
}

async function run() {
    console.log("Starting model tests...");
    // Test common models
    await testModel("gemini-1.5-flash");
    await testModel("gemini-1.5-flash-001");
    await testModel("gemini-1.5-flash-latest");
    await testModel("gemini-pro");
    await testModel("gemini-1.0-pro");
}

run();
