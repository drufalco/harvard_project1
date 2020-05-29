    <head>
        <title>Registration | Book Club</title>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.3/css/bootstrap.min.css" integrity="sha384-Zug+QiDoJOrZ5t4lssLdxGhVrurbmBWopoEl+M6BdEfwnCJZtKxi1KgxUyJq13dy" crossorigin="anonymous">
        <link rel="stylesheet" href="/static/css/project1.css">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
    </head>

    <nav class="navbar navbar-light">
        <a href="{{ url_for('home') }}" class="navbar-brand" id="brand">Book Club</a>
        <ul class="navbar-nav mr-auto">
            <li class="nav-item">
                <a href="{{ url_for('your_books') }}" id="your_books" class="nav-item nav-link">Your Books</a>
            </li>
        </ul>
        <form class="form-inline" action="{{ url_for('search') }}" method="POST">
            <input class="form-control mr-sm-2" type="text" placeholder="Search" aria-label="Search" name="search-keyword">
            <button class="btn btn-primary btn-outline-success my-2 my-sm-0 search" id="search_button" type="submit">Search</button>
        </form>
        <form class="form-inline" action="{{ url_for('logout') }}" method="POST">
            <button class="btn btn-outline-success" type="submit" id="logout">{{ log_message }}</button>
        </form>
      </nav>

    <body>
        <div class="container">
<h1>Register for an account here!</h1>

<form action="{{ url_for('register') }}" method="post">
    <div class="form-group">
        <label for="first_name">First name</label>
        <input type="text" class="form-control" name="first_name">
      </div>
    <div class="form-group">
      <label for="username">Email address</label>
      <input type="email" class="form-control" name="username" aria-describedby="usernameTag">
      <small id="usernameTag" class="form-text text-muted">This is your username.</small>
    </div>
    <div class="form-group">
      <label for="password">Password</label>
      <input type="password" class="form-control" name="password">
      <small id="usernameTag" class="form-text text-muted">Please use a unique password as this information is NOT encrypted.</small>
    </div>
    <button type="submit" class="btn btn-primary search">Submit</button>
</form>

<h2>Already have an account? Log in <a href="{{ url_for('login') }}">here.</a></h2>

</div>
</body>
