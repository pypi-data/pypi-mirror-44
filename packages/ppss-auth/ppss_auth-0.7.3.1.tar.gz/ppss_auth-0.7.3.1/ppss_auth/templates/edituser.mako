<%inherit file="${context['midtpl']}" />

<%
usergroups = {}
for g in user.groups:
    usergroups[g.id] = g.name
%>
<div class="row">
    <div class="col-xs-12 col-sm-6">
        <form action="${request.route_url('ppss:user:edit',elementid=userid)}" method="POST">
            
            <input class="form-control" type="text" name="username" placeholder="username" value="${user.username if user else ""}">
            </br>
            <input class="form-control" type="password" name="password" placeholder="password" value="">
            <div class="checkbox">
                <label for="enablecheck">
                    <input id="enablecheck" type="checkbox" value="1" checked="checked" name="enabled"> Enable:
                </label>
            </div>
            ## <select multiple name="allgroups" class="form-control">
            ##     %for g in allgroups:
            ##         <option value="${g.id}" ${"selected" if g.id in usergroups else ""}>${g.name}</option>
            ##     %endfor
            ## </select>
            %for g in allgroups:
                <label class="checkbox-inline">
                    <input name="allgroups" type="checkbox" value="${g.id}" ${"checked" if g.id in usergroups else ""}> ${g.name}
                </label>
            %endfor
            </br>
            <input class="btn btn-success" type="submit" name="submit" value="Apply"/>

            <p>${msg}</p>
        </form>
    </div>
</div>