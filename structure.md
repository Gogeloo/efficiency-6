efficiency-6
├── app - This is the main directory for our FastAPI application.
│   ├── main.py - This is the entry point of our FastAPI application. Here, we define our routes and start our application.
│   ├── api - This directory contains our API endpoints.
│   │   ├── __init__.py
│   │   ├── computercraft - This directory contains the API endpoints for the computers in Minecraft to communicate with each other.
│   │   │   ├── __init__.py
│   │   │   ├── computercraft.py - Endpoints for the computers in Minecraft to communicate with each other
│   │   │   ├── lua_files.py - Endpoints for managing Lua files
│   │   │   └── static_files.py - Endpoints for managing static files
│   │   └── models - Pydantic models for our application
│   │       ├── __init__.py
│   │       ├── computercraft_models.py
│   │       └── lua_models.py
│   ├── services - Business logic modules
│   │   ├── __init__.py
│   │   └── computercraft_service - Computercraft-related logic
│   │       ├── __init__.py
│   │       ├── navigation - Navigation logic
│   │       │   └── locate.py
│   │       └── refuling - Refuling logic
│   │           └── cole.py
    ├── utils - Utility modules
│   │   ├── __init__.py
│   │   ├── common.py - Common utility functions
│   │   ├── favicon.py - Favicon router
│   │   ├── rate_limit.py - Rate limiting middleware
│   │   ├── robots.py - Robots.txt router
│   │   ├── auth.py - Authentication methods (IF WE WANT)
│   │   └── sitemap.py - Sitemap router
│   └── frontend - Frontend application folder
│       ├── templates - HTML templates
│       │   └── index.html
│       ├── tailwindcss - Tailwind CSS setup
│       │   ├── package.json
│       │   ├── tailwind.config.js
│       │   └── styles.css
│       │       └── style.css
│       └── static - Static files (CSS, JS)
│           ├── styles.css - Tailwind CSS styles
│           └── main.js - JavaScript code
├── tests - All our pytest or unittest tests
│   ├── __init__.py
│   ├── test_main.py - Tests related to the main parts of the application
│   ├── test_computercraft.py
│   ├── test_pydantic_version.py
│   └── test_user_management.py
├── tailwind.config.js - This is the configuration file for Tailwind CSS. Here, we can customize our design system.
├── postcss.config.js - This is the configuration file for PostCSS, a tool for transforming CSS with JavaScript, which is used by Tailwind.
├── package.json - This file lists the Node.js dependencies of our frontend application, including Tailwind CSS and PostCSS.
├── Dockerfile - This file contains the instructions to Dockerize our application.
├── .pre-commit-config.yaml - This file contains the configuration for pre-commit hooks.
├── requirements.txt - This file lists the Python dependencies of our application.
└── README.md - This file contains the documentation of our project.