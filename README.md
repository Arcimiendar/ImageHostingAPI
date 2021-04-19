# ImageHostingApplication
### Default account plans 
Default account plans "Enterprise", "Premium", "Basic" had to be created by default. 
So It was added to the migration 

### ExpirbleLink
So that user can only create expirable link for their own images, 
the Creator field was removed.

### PK magic number problem
One of the solution is consideration, that the name is a primary key. 
The problems can apear when we want to rename the account plan. Also it will be
problematic to create account plan with duplicate name when we need to 
(for example, the same name in different countries).
So solution which I selected is creation of variables, that contains
ids of standart account plans. 
Considering, that all of those three plans have to exist before the application
starts, this is the best solution I found. Othervise it makes sense to just load them through fixtures and
remove from migrations.
