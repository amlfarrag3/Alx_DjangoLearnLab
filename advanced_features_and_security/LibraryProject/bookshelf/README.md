# Permissions and Groups

## Custom Permissions (defined in Book model):
- `can_view`: View books
- `can_create`: Create books
- `can_edit`: Edit books
- `can_delete`: Delete books

## User Groups:
- **Viewers**: can_view
- **Editors**: can_view, can_create, can_edit
- **Admins**: Full access (can_view, can_create, can_edit, can_delete)

## Usage in Views:
Use Django's `@permission_required` to protect views.

Example:
```python
@permission_required('bookshelf.can_edit', raise_exception=True)
