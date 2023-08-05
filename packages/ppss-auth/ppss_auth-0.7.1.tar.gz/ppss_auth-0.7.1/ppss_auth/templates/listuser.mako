<%inherit file="${context['midtpl']}" />

<table class="table">
	<thead>
		<tr>
			<th>Username</th>
			<th>Enabled</th>
			<th>Last access</th>
			<th>Action</th>
		</tr>
	</thead>
	<tbody>
		%for i,e in enumerate(elements):
			<tr>
				<td>${e.username}</td>
				<td>${"Yes" if e.enabled else "No"}</td>
				<td>${e.lastlogin.strftime('%Y-%m-%d') if e.lastlogin else " - "}</td>
				<td>
					<a class="btn btn-success" href="${request.route_url('ppss:user:edit',elementid=e.id)}">modify</a><br/>
					<!--a href="${request.route_url('ppsschangepassword',userid=e.id)}">modify</a><br/-->

				 </td>
			</tr>
		%endfor

	</tbody>


</table>

<div>
	<a class="btn btn-success" href="${request.route_url('ppss:user:edit',elementid = -1)}">Add User</a>
</div>