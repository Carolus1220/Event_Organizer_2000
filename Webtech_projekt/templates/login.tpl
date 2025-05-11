<html>

<head>
    <title>Login</title>
    <meta charset="UTF-8">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.6/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-4Q6Gf2aSP4eDXB8Miphtr37CMZZQ5oXLH2yaXMJ2w8e2ZtHTl7GptT4jmndRuHDT" crossorigin="anonymous">
</head>

<script>
    function visibility() {
        let x = document.getElementById('password');

        if (x.type === 'password') {
            x.type = 'text';
        } else {
            x.type = 'password';
        }
    }

</script>

<body class="bg-secondary">
    <div style="height: 75%" class="container bg-light w-50 shadow">
        <div class="row my-3 justify-content-start align-items-center">
            <div class="col-5 text-start">
                <a href="/" class="">Back to main menu</a>
            </div>
        </div>
        % if new_signup:
            <div class="row my-3 justify-content-center align-items-center">
                <div class="col-5 text-start">
                    <p class="text-success">New account created!</p>
                </div>
            </div>
        % end
        <div class="row mt-4 justify-content-center align-items-center">
            <div class="col-5 text-center">
                <h4 class="text-primary">Please login</h3>
            </div>
        </div>
        % if attend_error:
            <div class="row my-3 justify-content-center align-items-center">
                <div class="col-5 text-start">
                    <p class="text-danger">Can't add attendance if you are not logged in!</p>
                </div>
            </div>
        % end
        % if failed == True:
            <div class="row my-2 justify-content-center align-items-center">
                <div class="col-5 text-start text-justify">
                    <p class="text-danger">Wrong password</p>
                </div>
            </div>
        % end
        % if reset_pass:
            <div class="row my-3 justify-content-center align-items-center">
                <div class="col-5 text-start">
                    <p class="text-success">Password successfully reset!</p>
                </div>
            </div>
        % end
        <div class="row mb-3 mt-0 justify-content-center align-items-center">
            <div class="col-5 text-start">
                <form action="/login" method="post" id="login_form">
                    <input name="username" id="username" placeholder="Username" class="w-100 mb-2"><br>
                    <input name="password" id="password" type="password" placeholder="Password" class="w-100 my-2">
                    <input type="checkbox" onclick=visibility()>Show password
                </form>
            </div>
        </div>
        <div class="row my-3 justify-content-center align-items-center">
            <div class="col-5 text-center">
                <button type="submit" form="login_form" style="width: 100%;" class="btn btn-outline-primary">Login</button>
            </div>
        </div>
        <div class="row my-3 justify-content-center align-items-center">
            <div class="col-3 text-center">
                <a href="/help">Forgot you password?</a>
            </div>
            <div class="col-2 text-center">
                <a href="/sign_up">Sign up</a>
            </div>
        </div>
    </div>
</body>

</html>
