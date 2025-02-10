# LeetCode Review System

A spaced repetition system for LeetCode problems based on the Ebbinghaus Forgetting Curve.

## Overview
This project helps users systematically review LeetCode problems using the Ebbinghaus Forgetting Curve. The system automatically schedules reviews and sends email reminders to help users maintain their problem-solving skills.

## Features

### Current Features
- ✅ User authentication system
- ✅ Add LeetCode problems to review list
- ✅ Smart review scheduling based on Ebbinghaus Forgetting Curve
- ✅ Problem statistics and progress tracking
- ✅ Review management (complete/postpone reviews)
- ✅ Responsive web interface

### Core Functionality
- **Smart Scheduling**: Uses spaced repetition with intervals of 1, 2, 4, 7, and 15 days
- **Problem Management**: Easy addition and tracking of LeetCode problems
- **Progress Tracking**: Statistics and insights about your review progress
- **User Settings**: Customize notification time and timezone

## Tech Stack

### Frontend
- React 18 with TypeScript
- TailwindCSS for styling
- React Query for data fetching
- React Router for navigation
- Axios for API requests

### Backend
- FastAPI (Python)
- PostgreSQL for data storage
- Redis for caching
- SQLAlchemy ORM
- JWT authentication
- Pydantic for data validation

## Getting Started

### Prerequisites
- Python 3.11+
- Node.js 20+
- PostgreSQL 15+
- Redis 7+

### Local Development Setup

1. Clone the repository
```bash
git clone https://github.com/yourusername/leetcode-review.git
cd leetcode-review
```

2. Set up the backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
```

3. Configure environment variables
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Set up the database
```bash
alembic upgrade head
```

5. Start the backend server
```bash
uvicorn app.main:app --reload
```

6. Set up the frontend
```bash
cd frontend
npm install
```

7. Start the frontend development server
```bash
npm run dev
```

## Roadmap

### Phase 1 (Current)
- [x] Basic authentication system
- [x] Problem management
- [x] Review scheduling
- [x] Basic statistics

### Phase 2 (Next)
- [ ] Email notification system
- [ ] Problem notes and solutions
- [ ] Review history and analytics
- [ ] Mobile-responsive design improvements
- [ ] Problem tags and categorization

### Phase 3 (Future)
- [ ] Problem difficulty prediction
- [ ] Review performance tracking
- [ ] Social features (share progress, compete with friends)
- [ ] Integration with LeetCode API
- [ ] Custom review intervals
- [ ] Problem recommendation system

### Phase 4 (Long-term)
- [ ] Mobile app development
- [ ] AI-powered review suggestions
- [ ] Problem solution templates
- [ ] Code execution environment
- [ ] Integration with other platforms (HackerRank, CodeForces)

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## Development Guidelines
- Follow PEP 8 for Python code
- Use TypeScript for all frontend code
- Write tests for new features
- Update documentation when making changes

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
- Inspired by the Ebbinghaus Forgetting Curve
- Built with modern web technologies
- Thanks to the open-source community
