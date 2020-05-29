
{% extends "layout.html" %}

{% block title %}
Registration
{% endblock %}

{% block body %}
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

{% endblock %}
