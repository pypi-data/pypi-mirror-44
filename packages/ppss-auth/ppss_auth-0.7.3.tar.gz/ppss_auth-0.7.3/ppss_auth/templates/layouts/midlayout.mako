<%inherit file="${context['supertpl']}" />


<div class="usermenu">
	<ul>
		<li class="${'active' if activemenu=='user' else ''}"><a href="${request.route_url('ppss:user:list')}"> Users</a></li>
		<li class="${'active' if activemenu=='group' else ''}"><a href="${request.route_url('ppss:group:list')}">Groups</a></li>
		<li class="${'active' if activemenu=='perm' else ''}"><a href="${request.route_url('ppss:perm:list')}"> Permissions</a></li>
	</ul>

</div>
<div>


${next.body()}
</div>