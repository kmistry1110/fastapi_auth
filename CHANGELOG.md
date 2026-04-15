# Changelog

All notable changes to this project will be documented in this file.

---

## [0.1.0] - 2026-03-31

### Added
- Initial release of `fastapi-async-auth-kit`
- User authentication endpoints:
  - Register
  - Login
  - Logout
- JWT-based authentication (access + refresh tokens)
- Token validation middleware / dependencies
- Async-ready authentication flows
- Secure password hashing
- Environment-based configuration support

### Security
- Basic JWT signature validation
- Password hashing with salt

---

## [0.2.0/0.3.0/0.4.0/0.5.0/0.6.0] - 2026-04

### Changed
- Minor changes around readme pytoml files

---

## [0.7.0/0.8.0] - 2026-04-15

### Changed
- Added changelog file
- Added github links in pyproject.toml file


---

## Notes

- Dates follow ISO format (YYYY-MM-DD)
- Versions follow semantic versioning:
  - MAJOR: Breaking changes
  - MINOR: New features
  - PATCH: Bug fixes