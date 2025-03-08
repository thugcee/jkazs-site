#!/bin/bash

echo Page: http://localhost:1313
echo CMS: http://localhost:1313/admin/

npx decap-server &
hugo serve
