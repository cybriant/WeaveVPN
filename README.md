# WeaveVPN

Virtual Private Networks (VPNs) are an important tool in networking infrastructure and OpenVPN is the most
prolific and robust open source framework for VPN connectivity. In theory, OpenVPN allows the set up of a
Software Defined Network (SDN), connecting many different VPNs together. However in practice this is
difficult to accomplish. WeaveVPN is a web based service for dynamically setting up and configuring an
SDN, quickly, easily, and securely.

# Technology Stack
- Vue.js
- Flask (Python)
- MariaDB
- Linux - CentOS
- OpenVPN
- OAuth2.0 Security Specification


# How to Set Up Backend

1. Change directory to Backend directory: 
   - `cd Backend`

2. Install dependencies first from requirements.txt 
    - Using Python: `pip install -r requirements.txt`
    - Using Python3: `pip3 install -r requirements.txt`

3. Change directory to the Auth Server directory: 
   - `cd auth_server`

4. Create database and run development server: 
    - `python app.py`

# How to Set Up Frontend

1. Change directory to Frontend directory: 
     - `cd Frontend`

2. Install dependencies: 
    - Using yarn (recommended): `yarn install`
    - Using npm: `npm install`

3. Development build (local):
    - Using yarn (recommended): `yarn serve`
    - Using npm: `npm run dev`

4. Production build:
    - Using yarn (recommended): `yarn build`
    - Using npm: `npm run build`


To install yarn go here: (https://classic.yarnpkg.com/en/docs/install).

To install npm go here: (https://www.npmjs.com/get-npm).
