<html>

<head>
    <title>Create an event</title>
    <meta charset="UTF-8">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.6/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-4Q6Gf2aSP4eDXB8Miphtr37CMZZQ5oXLH2yaXMJ2w8e2ZtHTl7GptT4jmndRuHDT" crossorigin="anonymous">
    <style>
        input:invalid + span::after {
            content: " ✖";
        }

        input:valid + span::after {
            content: " ✓";
        }
    </style>
</head>

<script>
    
</script>

<body class="bg-secondary">
    <div style="height: 75%" class="container bg-light w-50 shadow">
        <div class="row my-3 justify-content-start align-items-center">
            <div class="col-5 text-start">
                <a href='/'>Back to main menu</a>
            </div>
        </div>
        <div class="row my-3 justify-content-center align-items-center">
            <div class="col-5 text-center">
                <h4 class="text-primary">Create a new event</h4>
            </div>
        </div>
        <div class="row my-3 justify-content-center align-items-center">
            <div class="col-5 text-start">
                <form action='/create' method='post' id="create_form">
                    <input name='name' placeholder="Event's name" class="w-100 mb-2" required><br>
                    <label class="w-10">Date of the event:</label>
                    <input name='date' type='date' max='2028-12-31' min='2025-01-01' class="w-85 my-2" required>
                    <span class="validity w-5 text-end"></span><br>
                    <input name='location' placeholder="Location" class="w-100 my-2" required><br>
                    <input name='fee' placeholder="Entry fee" class="w-100 mt-2" required><br>
                </form>
            </div>
        </div>
        <div class="row my-3 justify-content-center align-items-center">
            <div class="col-5 text-start">
                <button type="submit" form="create_form" class="btn btn-outline-primary w-100">Create event</button>
            </div>
        </div>
    </body>
</body>

</html>