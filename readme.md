# Medical Image Processing Project

This repository contains multiple components for medical image processing and analysis.

## Project Structure

- **punto_1**: Hanoi Tower implementation with colorization
- **punto_2**: File processing utilities
- **punto_3**: Backend API for medical data analysis
  - Python Flask application
  - Database integration
  - Statistical analysis tools
- **punto_4**: Stain Area Calculator
  - Angular web application
  - Image processing features

## Requirements

### Backend (punto_3)

- Python 3.x
- PostgreSQL
- Required Python packages:
  - Flask
  - SQLAlchemy
  - pandas
  - numpy
  - python-dotenv
- Create a `.env` file in the backend directory (punto_3) with the following configuration:
```env
DATABASE_USERNAME=USERNAME
DATABASE_PASSWORD=PASSWORD
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=DB_NAME
DEBUG_MODE=True
```
### Frontend (punto_4)

- Node.js
- Angular CLI 19.0.6
- Required npm packages:
  - @angular/cli
  - tailwindcss
  - html2canvas
  - ngx-file-drop

## Installation

1. Clone the repository:

```bash
git clone https://github.com/juandiegou/imexhs.git
```

2. Set up the backend:

```bash
cd punto_3
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up the frontend:

```bash
cd punto_4/stain-area-calculator
npm install
```

## Running the Applications

### Backend API (punto_3)

```bash
cd punto_3
source venv/bin/activate  # On Windows: venv\Scripts\activate
python -m app.main
```

### Stain Area Calculator (punto_4)

```bash
cd punto_4/stain-area-calculator
ng serve
```

Access the application at `http://localhost:4200`

## Testing

### Backend Tests

```bash
cd punto_3
pytest
```

## License

Unlicensed - see [LICENSE](LICENSE) for more information.

## Contributors

Juan Diego Gallego Giraldo - [juandiegougallego@hotmail.com](mailto: juandiegougallego@hotmail.com)

```

This README includes:
1. Project overview and structure
2. Requirements for both backend and frontend
3. Installation instructions
4. Running instructions
5. Testing procedures
6. Placeholders for license and contributors

```
