<%inherit file="${context['midtpl']}" />

<div class="row">
    <div class="col-xs-12 col-sm-6">
        <form action="${request.route_url('ppss:perm:edit',elementid=perm.id)}" method="POST">    
            <input class="form-control" type="text" name="name" placeholder="permissionname" value="${perm.name}">
            <br/>
            <input class="btn btn-success" type="submit" name="submit" value="Apply"/>
        </form>
    </div>
</div>