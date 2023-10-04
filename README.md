# Blockchain Visualization Project

## Overview

This project is aimed at visualizing the relationships between blockchain wallets using a graph-based approach. Each wallet is represented as a node in the graph, and the relationships between wallets are established to provide insights into the transaction flows within the blockchain. The goal is to create an intuitive and interactive user interface for exploring wallet relationships and transaction details.

## Our Team

Meet the talented individuals behind this project:

- **Felix Joshua**: Project Lead
- **Darrel Devlin**: Data Analyst
- **Bryan Oscarina**: Security Admin

## Technologies Used

- **Frontend**: We utilize D3.js for rendering the graph visualization and React.js as our frontend framework.
- **Backend**: The backend is developed using Python, and we use the Neo4j graph database to store and query blockchain data efficiently.
- **API**: FastAPI is employed to create a RESTful API for serving data to the frontend. Axios is used for making HTTP requests from the frontend to the backend API.

## Features

- **Graph Visualization**: The core feature of this project is the graph visualization of blockchain wallet relationships. Wallets are represented as nodes, and relationships are established based on transaction data.

- **Search by Address**: Users can search for specific wallets by their address. This feature provides a quick way to locate and explore individual wallets.

- **Transaction Details (1 Hop)**: Users can view transaction details for a selected wallet, including one-hop transactions. This allows users to see which wallets are directly connected to the selected one.

- **Interactive Exploration**: Clicking on nodes within the graph allows users to traverse the blockchain by exploring related wallets. This interactive feature enhances the user's ability to understand transaction flows and relationships.

## Getting Started

1. **Prerequisites**: Ensure you have the following software installed on your system:
   - Node.js and npm (for frontend)
   - Python (for backend)
   - Neo4j (for the graph database)
2. **Clone the Repository**: Clone this repository to your local machine:

   ```bash
   git clone https://github.com/your-username/blockchain-visualization.git
   cd blockchain-visualization
   ```

3. **Frontend Setup**:

   - Navigate to the `frontend` directory and install dependencies:

     ```bash
     cd frontend
     npm install
     ```

   - Start the frontend development server:

     ```bash
     npm start
     ```

4. **Backend Setup**:

   - Navigate to the `backend` directory and install Python dependencies (consider using a virtual environment):

     ```bash
     cd backend
     pip install -r requirements.txt
     ```

   - Configure the Neo4j database connection in `backend/config.py`.

   - Start the FastAPI server:

     ```bash
     uvicorn main:app --host 0.0.0.0 --port 8000 --reload
     ```

5. **Access the Application**: Open your web browser and navigate to `http://localhost:3000` to access the blockchain visualization website.

6. **Database Setup**: Ensure Neo4j is installed and running. Configure the database connection details in the `backend/config.py` file.

7. **Initialize the Database**: Populate your Neo4j database with the necessary blockchain data. You may need to write scripts or utilize ETL (Extract, Transform, Load) processes to import blockchain data into Neo4j.

8. **Access the Application**: Once the frontend and backend are set up, you can access the blockchain visualization website by opening your web browser and navigating to `http://localhost:3000`.

## Deployment

When deploying this application to a production environment, make sure to configure production settings, such as using a production-ready database, setting up secure connections, and optimizing for performance.

## Contributing

Contributions to this project are welcome. If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix: `git checkout -b feature/your-feature-name`.
3. Make your changes and commit them: `git commit -m "Add your feature description"`.
4. Push your changes to your fork: `git push origin feature/your-feature-name`.
5. Create a pull request to the `main` branch of the original repository.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or inquiries, please contact Felix Joshua at [felixjoshuaa@gmail.com].
