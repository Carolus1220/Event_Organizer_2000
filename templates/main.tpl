<html>

<head>
    <title>Kezdőlap</title>
    <meta charset="UTF-8">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.6/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-4Q6Gf2aSP4eDXB8Miphtr37CMZZQ5oXLH2yaXMJ2w8e2ZtHTl7GptT4jmndRuHDT" crossorigin="anonymous">
</head>
    

<script>
    
</script>

<body>
    <div class="container-fluid">
        <div class="row bg-light px-3 pt-1 border-bottom border-2 border-secondary">
            % if logged:
                <div class="col-9">
                    <p class="text-start">Event Organizer 2000</p> 
                </div>
                <div class="col-2">
                    <p class="text-end">Logged in as {{logged}}</p>
                </div>
                <div class="col-1 justify-content-start">
                    <a href="/logout" class="">Logout</a>
                </div>
            % else:
                <div class="col-11">
                    <p class="text-start">Event Organizer 2000</p>
                </div>
                <div class="col-1">
                    <a href="/login" class="nav-link text-end">Login</a>
                </div>
            % end
        </div>
        % if logged:
            <div class="row">
                <div class="col">
                    <h2 class="">Your events</h2>
                </div>
                % if new_event:
                    <div class="col">
                        <p class="text-success">New event created!</p>
                    </div>
                % end
                % if new_attendance:
                    <div class="col">
                        <p class="text-success">New attendance added!</p>
                    </div>
                % end
                % if attend_error:
                    <div class="col">
                        <p class="text-danger">Can't add attendance!</p>
                    </div>
                % end
                % if rm_attend:
                    <div class="col">
                        <p class="text-success">Removed attendance!</p>
                    </div>
                % end
                <div class="col">
                    <a href="/create">Create new</a>
                </div>
            </div>
            <div class="row">
            % if your_events != []:
            % for event in your_events:
            % creator, date, name, location, fee = event[0], event[1], event[2], event[3], event[4]
                <div class="col">
                    <div class="card" style="width: 15rem; height: 16rem;">
                        <div class="card-header">
                            <h5 class="card-title">{{name}}</h5>
                            <h6 class="card-subtitle text-muted">Created by: {{creator}}</h6>
                        </div>
                        <div class="card-body">
                            <p class="card-text">Date: {{date}}</p>
                            <p class="card-text">Location: {{location}}</p>
                            <p class="card-text">Entry fee: {{fee}}</p>
                        </div>
                        <div class="card-footer text-center">
                            <a href="/unattend?id={{event[-1]}}" class="card-link btn btn-outline-primary">Un-attend</a>
                        </div>
                    </div>
                </div>
            % end
            % else:
                <p>No events to display</p>
            % end
            </div>
                
        % end
        <div class="row justify-content-center">
            <div class="col text-start">
                <h2 class="">All events</h2>
            </div>
        </div>
        <div class="row">
            % if all_events != []:
            % for event in all_events:
            % creator, date, name, location, fee = event[0], event[1], event[2], event[3], event[4]
                <div class="col">
                    <div class="card">
                        <div class="card-header">
                            <h5 class="card-title">{{name}}</h5>
                            <h6 class="card-subtitle text-muted">Created by: {{creator}}</h6>
                        </div>
                        <div class="card-body">
                            <p class="card-text">Date: {{date}}</p>
                            <p class="card-text">Location: {{location}}</p>
                            <p class="card-text">Entry fee: {{fee}}</p>
                        </div>
                        <div class="card-footer text-center">
                            <a href="/attend?id={{event[-1]}}" class="card-link btn btn-outline-primary">Attend</a>
                        </div>
                    </div>
                </div>
            % end
            % else:
                <p>No events to display</p>
            % end
            </div>
    </div>
</body>

</html>