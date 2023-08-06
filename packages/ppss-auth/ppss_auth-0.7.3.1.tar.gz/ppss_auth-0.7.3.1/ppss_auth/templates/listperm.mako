<%inherit file="${context['midtpl']}" />

<table class="table">
	<thead>
		<tr>
			<th>Nome</th>
			<th>Sistema</th>
		</tr>
	</thead>
	<tbody>
		%for i,e in enumerate(elements):
			<tr>
				<td>${e.name}</td>
				<td>${"Yes" if e.permtype == 1 else "No"}</td>
				<td>
					<a class="btn btn-success" href="${request.route_url('ppss:perm:edit',elementid=e.id)}">delete</a><br/>
					<!--a href="${request.route_url('ppsschangepassword',userid=e.id)}">modify</a><br/-->

				 </td>
			</tr>
		%endfor

	</tbody>


</table>

<div>
	<a class="btn btn-success" href="${request.route_url('ppss:perm:edit',elementid = -1)}">Add Perm</a>
</div>