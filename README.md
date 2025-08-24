# Library Management System

A Django REST Framework-based project for managing a library's books, genres, borrowing records, and user authentication.

---

## 🚀 Features

- **Genre Management**  
  - CRUD operations for genres.
- **Book Management**  
  - CRUD operations for books.
  - Search, filter, and pagination.
- **Borrowing Records**  
  - Track who borrowed which books and manage due dates.
  - Mark records as returned or overdue.
  - List all overdue borrowing records.
- **User Authentication & Registration**  
  - Register new users.
  - Login and obtain auth token.
- **User Groups & Members**  
  - List user groups.
  - List members (users in "Member" group).
- **Permissions & Security**  
  - Token-based authentication required for protected endpoints.
  - Role-based access using Django groups.
- **Filtering, Ordering, and Pagination**  
  - Filter books/records by fields.
  - Search by title, author, genre, member name.
  - Order by borrow date, due date, status.

---

## 🛠 Tech Stack

- **Backend:** Python, Django, Django REST Framework
- **Authentication:** Django REST Framework Token Auth
- **Filtering & Search:** django-filter, DRF SearchFilter/OrderingFilter
- **Database:** Django ORM (default: SQLite, configurable)
- **Other:** Django Admin, Django Groups

---

## 📁 Project Structure

```
libary_management_system/
├── Libary_management_system/
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── baseApp/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── views.py
│   └── __init__.py
├── manage.py
└── README.md
```

---

## 🌐 API Endpoints

| Endpoint                            | Method | Description                                        | Auth Required |
|--------------------------------------|--------|----------------------------------------------------|--------------|
| `/genres/`                          | GET/POST | List or create genres                              | Yes          |
| `/genres/{id}/`                     | GET/PUT/DELETE | Retrieve, update, delete genre                    | Yes          |
| `/books/`                           | GET/POST | List, search, filter, create books                 | Yes          |
| `/books/{id}/`                      | GET/PUT/DELETE | Retrieve, update, delete book                     | Yes          |
| `/borrow-records/`                  | GET/POST | List, filter, create borrow records                | Yes          |
| `/borrow-records/{id}/`             | GET/PUT/DELETE | Retrieve, update, delete borrow record            | Yes          |
| `/borrow-records/{id}/return/`      | POST   | Mark borrow record as returned                     | Yes          |
| `/borrow-records/{id}/overdue/`     | POST   | Mark borrow record as overdue                      | Yes          |
| `/borrow-records/overdue/`          | GET    | List all overdue borrow records                    | Yes          |
| `/register/`                        | POST   | Register a new user                               | No           |
| `/login/`                           | POST   | User login, obtain authentication token            | No           |
| `/groups/`                          | GET    | List all user groups                              | Yes          |
| `/members/`                         | GET    | List all members (users in "Member" group)         | Yes          |
| `/members/{id}/`                    | GET    | Get details of a specific member                   | Yes          |
| `/admin/`                           | -      | Django admin interface                             | Yes          |

> **Note:** Most endpoints require token authentication except `/register/` and `/login/`.

---

## 📄 Postman API Documentation

- [Postman Collection Link](#)  
https://documenter.getpostman.com/view/33338845/2sB3BGHpns
---

## 📚 Usage

- Use the `/register/` endpoint to create a new account.
- Login via `/login/` to obtain your token.
- Use the token in the `Authorization: Token <your-token>` header for authenticated endpoints.

---

## 💡 Contributing

Feel free to open issues or pull requests for improvements or bug fixes.

---

## 📝 License

MIT

