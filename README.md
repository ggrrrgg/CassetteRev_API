<h1>George Sheridan API Webserver Project</h1>

Github: https://github.com/ggrrrgg/CassetteRev_API

Trello board: https://trello.com/b/lYuECRJh/georgesheridant2a4api

<h3>Installation Instructions</h3>

Download or clone the repository from github link provided above.

You will need recent versions of Python3 and postgresql installed.

Open a terminal instance and enter 

```sudo service postgresql start``` to start the server

then

```sudo -u postgres psql``` (for windows/wsl)

Then create a user and set password

```CREATE USER cassette_rev_dev WITH PASSWORD '123456'```

Create the database

```CREATE DATABASE cassette_rev WITH OWNER= cassette_rev_dev```

Grant yourself priveledges to use the database

```GRANT ALL PRIVILEGES ON DATABASE cassette_rev TO cassette_rev_dev```

Check it has worked by typing

```\l```

Then connect to the database

```\c cassette_rev;```

In another terminal instance navigate to the src folder and create/activate a virtual environment

```python3 -m venv .venv```

```source .venv/bin/activate```

Install the requirements

```pip3 install -r requirements.txt```

Then run the following commands to create the tables, and seed them with some data (admin user is created here)

```flask db create```

```flask db seed```

You can then check the postgres terminal instance to see this has worked by typing ```\dt``` and you should see the 4 tables there.

Finally run the app

```flask run```

---
<h3>R1 Problem</h3>

There are, out there people who still love to buy and listen to music on cassette. It has its appeals, like vinyl, owning a physical, tangible copy of an album that you love that has great artwork and liner notes to explore as you listen is a much more immersive experience than listening to streaming services. Cassettes are loved for their nostalgic quality (to certain generations) and the sonic imprint the medium imparts is comfortable to listen to, and compliments many styles of music (lofi electronic music and ambient music are strong modern genres).

There are not many places online that cater to this community and what is available is scattered between reddit threads and personal bloggers. A more central app that is able to keep up to date with new releases and provide a space for enthusiasts to share their own discoveries could be a great resource for that community.

<h3>R2 Why</h3>

The hope would be that in providing a space for the cassette loving community to come together the community grows, pulling in people new to the format. Encouraging a more relaxed and linearly focused way to enjoy music is a small dose, but a healthy antidote to the scattered attention lifestyle of the current smartphone / internet age.

This version of the app is intended as a simple framework of what it could become, admin users are able to add releases to keep users up to date with the latest. Users are then able to discuss those releases by leaving reviews and commenting on eachothers reviews. Users can also add their own discovered releases. More detail can be added around the specifics of the cassette pressing, tape type quality, and reissue details etc in their review if they wish. I'd like to integrate a bandcamp API to provide artwork and streaming and a link to purchase, but I ran out of time unfortunately.

<h3>R3 Why PostgreSQL</h3>

I have used PostgreSQL for this project, it has these advantages:

<i>Transactions</i> - PostgreSQL provides transactional DDL, allowing complex relational applications to make changes to both the application and the database schema within a single transaction, eliminating the need for extensive error handling code.

<i>Code comments</i> - PostgreSQL allows code comments, enabling better understanding of code functionality and facilitating collaboration which is important for any future the app may have.

<i>Data Integrity</i> - PostgreSQL is known for its data integrity, thanks to its ACID compliance that ensures reliable data storage, retrieval, and management.

<i>Scalability</i> - PostgreSQL can handle large datasets with ease and can scale up or down as per business needs without compromising data integrity or performance.

<i>Great Community</i> - PostgreSQL has a vibrant and enthusiastic community of developers, users, and contributors that continually improve the database and provide excellent support to users worldwide.

<i>Extensibility</i> - PostgreSQL is highly extensible, allowing users to add additional features, functions, data types, and languages to the database. It provides a packaging tool for installing add-ons and supports a wide range of languages, including JavaScript.

<i>Security features</i> - PostgreSQL includes built-in security features and allows the use of extensions to enhance security. It offers parameter security and application security, allowing for fine-grained control over user privileges and access permissions.

<b>Disadvantages of PostgreSQL:</b>

<i>Database structure</i> - PostgreSQL follows a strict relational database structure, which requires predefined schemas and fields. Adding additional data attributes or changing the schema can be cumbersome compared to NoSQL databases like MongoDB, which have more flexible document-based structures.

<i>Open source</i> - Being open source, PostgreSQL lacks the backing of a single organization and may face challenges in terms of awareness, support, and compatibility. There is no warranty, liability protection, or indemnity for the software.

<i>Complexity</i> - PostgreSQL can be complex to set up and configure compared to other databases, but this can be overcome by using cloud-based services or managed hosting solutions that simplify the process.

<i>Fewer Tools</i> - Compared to other databases such as MySQL or Oracle, PostgreSQL has fewer tools available for monitoring, backup, and performance tuning, but there are still many third-party tools available to fill the gap.

<i>Slower performance</i> - PostgreSQL's relational structure can result in slower performance when querying large tables with many fields, as it needs to scan the entire table to find relevant data. Performance issues and backup recovery challenges may arise in certain scenarios.

PostgreSQL offers numerous advantages and disadvantages but remains a highly functional and widely used database system known for its robustness, reliability, and scalability, making it an excellent choice for this app.


<h3> ORM </h3>

An ORM (Object-Relational Mapping) is a programming technique that allows developers to interact with a relational database using an object-oriented programming language. It essentially bridges the gap between the object-oriented world of programming languages and the relational world of databases. 

In this case the ORM used is SQLAlchemy, bridging the gap between Python and PostgreSQL.

ORMs provide a higher-level abstraction over database operations. Instead of writing raw SQL queries, developers can work with objects and classes that directly represent database tables and relationships. 
For example in this app, database tables are represented as Python classes:

```
class Release(db.Model):
    __tablename__ = 'releases'
    id = db.Column(db.Integer, primary_key=True)
    artist = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    date_released = db.Column(db.Date)
    genre = db.Column(db.String)
```

An entry is then declared as a Python object:

```
Release(
            artist='de la soul',
            title='stakes is high',
            date_released='2/7/96',
            genre='Hip Hop',
        )
```

The postgres command for this entry would look like this
```
INSERT INTO releases (artist, title, date_released, genre)
VALUES ('de la soul', 'stakes is high', '1996-02-07', 'Hip Hop');
```

If we had to make every entry this way it would get very time consuming for large datasets and errors are typos are easily made.

Should note also that SQLalchemy is interchangable between DBMS's, we could use the same app with MySQL, SQLite without having to change the code significantly.

SQLAlchemy also simplifies the Create, Read, Update, and Delete (CRUD) operations. We can perform these using method calls on objects, without having to write raw SQL statements.

Additionally we can compose queries using high-level language constructs rather than dealing with SQL directly, making query construction more readable and maintainable.


Relationship Management:
Managing relationships between database tables can be complex. ORM frameworks handle these relationships transparently, allowing developers to easily define and work with relationships like one-to-one, one-to-many, and many-to-many. This simplifies working with complex data models.

Data Validation and Type Safety:
ORMs often include built-in data validation mechanisms. This helps enforce data integrity and ensures that the data stored in the database is consistent and valid. Additionally, ORMs provide type safety by mapping database columns to specific data types in the programming language.

Performance Optimization:
While ORMs abstract away the complexity of database operations, some ORMs also offer performance optimization features, such as lazy loading and query optimization. These features help in reducing unnecessary database calls and optimizing the performance of database operations.

Code Reusability:
ORMs allow developers to define data models and interact with data in a consistent manner across the application. This promotes code reusability as the same data models and operations can be utilized in different parts of the application.

Rapid Application Development (RAD):
Using an ORM can significantly speed up the development process. Developers can focus more on application logic and less on writing database-specific code. This results in faster development cycles and quicker time-to-market for applications.





