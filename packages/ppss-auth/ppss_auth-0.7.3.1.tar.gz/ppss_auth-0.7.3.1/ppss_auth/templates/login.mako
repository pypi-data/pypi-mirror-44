<%inherit file="${context['logintpl']}" />
<div class="row">
    <div class="col-xs-12 col-sm-6 col-sm-offset-3">
        <form action="${request.route_url('ppsslogin')}" method="POST">
            
            <input class="form-control" type="text" name="username" placeholder="username">
            <br/>
            <input class="form-control" type="password" name="password" placeholder="password">
            <br/>
            <div class="text-center">
                <input class="btn btn-success" type="submit" name="submit" value="entra"/>
            </div>
            </br>
            <p class="text-danger">${msg}</p>
        </form>
    </div>
</div>