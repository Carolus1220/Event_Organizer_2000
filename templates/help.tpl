<html>

<head>
    <title>Password recovery</title>
    <meta charset="UTF-8">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.6/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-4Q6Gf2aSP4eDXB8Miphtr37CMZZQ5oXLH2yaXMJ2w8e2ZtHTl7GptT4jmndRuHDT" crossorigin="anonymous">
</head>

<script>
    function visibility() {
        let x = document.getElementById('password');
        let y = document.getElementById('password2');

        if (x.type === 'password') {
            x.type = 'text';
            y.type = 'text';
        } else {
            x.type = 'password';
            y.type = 'password';
        }
    }

</script>

<body class="bg-secondary">
    <div  style="height: 75%" class="container bg-light w-50 shdaow">
        <div class="row my-3 justify-content-start align-items-center">
            <div class="col-5 text-start">
                <a href='/login'>Back to login menu</a>
            </div>
        </div>
        <div class="row mt-4 justify-content-center align-items-center">
            <div class="col-5 text-center">
                <h4 class="text-primary">Reset password</h4>
            </div>
        </div>
        % if error != '':
            <div class="row my-2 justify-content-center align-items-center">
                <div class="col-5 text-start">
                    <p style="color: red">{{!error}}</p>
                </div>
            </div>
        % end
        <div class="row mb-3 mt-0 justify-content-center align-items-center">
            <div class="col-5 text-center">
                <form action="/help" method="post" id="reset_form">
                    <input name="username" placeholder="Username" class="w-100 mb-2">
                    <input name="new_pass_1" type="password" placeholder="Password" id="password" class="w-100 my-2">
                    <input name="new_pass_2" type="password" placeholder="Password again" id="password2" class="w-100 my-2">
                    <input type="checkbox" onclick="visibility()">Show password(s)
                </form>
            </div>
        </div>
        <div class="row my-3 justify-content-center align-items-center">
            <div class="col-5 text-center">
                <button type="submit" form="reset_form" style="width: 100%;" class="btn btn-outline-primary">Reset password</button>
            </div>
        </div>
    </div>
</body>

</html>