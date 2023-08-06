<%inherit file="${context['midtpl']}" />

<table class="table">
	<thead>
		<tr>
			<th>Group name</th>
			<th>Permissions</th>
			<th>Enabled</th>
			
			<th>Action</th>
		</tr>
	</thead>
	<tbody>
		%for i,e in enumerate(elements):
			<tr>
				<td>${e.name}</td>
				<td>${", ".join([p.name for p in e.permissions])}</td>
				<td>${"Yes" if e.enabled else "No"}</td>
				<td>
					<a class="btn btn-success" href="${request.route_url('ppss:group:edit',elementid=e.id)}">modify</a><br/>
				 </td>
			</tr>
		%endfor

	</tbody>


</table>

<div>
	<a class="btn btn-success" href="${request.route_url('ppss:group:edit',elementid = -1)}">Add Group</a>
</div>