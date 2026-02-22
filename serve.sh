#!/bin/bash

echo "Building documentation with DocFx..."
docfx build

echo "Starting DocFx server on http://localhost:8080..."
docfx serve _site --port 8080