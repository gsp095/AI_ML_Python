Below is a minimal .NET Core C# API for performing CRUD operations on an Employee entity using an MS SQL database. The example includes the `Create` operation for adding employee data.

### Prerequisites
1. Install the .NET SDK.
2. Install the required NuGet packages:
   - `Microsoft.EntityFrameworkCore`
   - `Microsoft.EntityFrameworkCore.SqlServer`
   - `Microsoft.EntityFrameworkCore.Tools`

### Code Implementation

#### 1. Create the `Employee` Model
```csharp
public class Employee
{
    public int Id { get; set; }
    public string Name { get; set; }
    public string Position { get; set; }
    public decimal Salary { get; set; }
}

#### 2. Create the `AppDbContext`
```csharp
using Microsoft.EntityFrameworkCore;

public class AppDbContext : DbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }

    public DbSet<Employee> Employees { get; set; }
}

#### 3. Configure the Minimal API
```csharp
using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("DefaultConnection")));

var app = builder.Build();

// Map endpoints
app.MapPost("/employees", async (Employee employee, AppDbContext dbContext) =>
{
    dbContext.Employees.Add(employee);
    await dbContext.SaveChangesAsync();
    return Results.Created($"/employees/{employee.Id}", employee);
});

app.MapGet("/employees", async (AppDbContext dbContext) =>
    await dbContext.Employees.ToListAsync());

app.MapGet("/employees/{id}", async (int id, AppDbContext dbContext) =>
{
    var employee = await dbContext.Employees.FindAsync(id);
    return employee is not null ? Results.Ok(employee) : Results.NotFound();
});

app.MapPut("/employees/{id}", async (int id, Employee updatedEmployee, AppDbContext dbContext) =>
{
    var employee = await dbContext.Employees.FindAsync(id);
    if (employee is null) return Results.NotFound();

    employee.Name = updatedEmployee.Name;
    employee.Position = updatedEmployee.Position;
    employee.Salary = updatedEmployee.Salary;

    await dbContext.SaveChangesAsync();
    return Results.NoContent();
});

app.MapDelete("/employees/{id}", async (int id, AppDbContext dbContext) =>
{
    var employee = await dbContext.Employees.FindAsync(id);
    if (employee is null) return Results.NotFound();

    dbContext.Employees.Remove(employee);
    await dbContext.SaveChangesAsync();
    return Results.NoContent();
});

app.Run();

#### 4. Add Connection String in `appsettings.json`
```json
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=YOUR_SERVER_NAME;Database=EmployeeDb;Trusted_Connection=True;MultipleActiveResultSets=true"
  }
}

#### 5. Add Migrations and Update Database
Run the following commands in the terminal to create the database and apply migrations:
```bash
dotnet ef migrations add InitialCreate
dotnet ef database update

#### 6. Run the Application
Run the application using the following command:
```bash
dotnet run

You can now test the API using tools like Postman or cURL. The endpoints are:
- `POST /employees` - Create a new employee.
- `GET /employees` - Get all employees.
- `GET /employees/{id}` - Get a specific employee by ID.
- `PUT /employees/{id}` - Update an employee by ID.
- `DELETE /employees/{id}` - Delete an employee by ID.

This implementation follows OOP principles, is minimal, and adheres to best practices. You can extend it further as needed.