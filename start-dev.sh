#!/bin/bash

echo Page: http://localhost:1313
echo CMS: http://localhost:1313/admin/

echo disabled: npx decap-server
hugo server --noHTTPCache --renderToMemory
