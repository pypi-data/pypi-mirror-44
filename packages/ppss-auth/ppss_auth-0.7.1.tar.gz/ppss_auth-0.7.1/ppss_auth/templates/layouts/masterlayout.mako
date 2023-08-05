<html>
<head>
	<title>Login page</title>
	<link rel="stylesheet" href="${request.static_url('ppss_auth:ppss_auth_static/ppssauth.css')}" type="text/css" />
	<%block name="ppssautcss">

	</%block>

  <%block name="ppssauthheaderjs">
    <link
      rel="stylesheet"
      href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css"
      integrity="sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO"
      crossorigin="anonymous"
    />
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/handlebars.js/4.1.0/handlebars.min.js"></script>
    <script
          src="https://code.jquery.com/ui/1.12.1/jquery-ui.min.js"
          integrity="sha256-VazP97ZCwtekAsvgPBSUwPFKdrwD3unUfSGVYrahUqU="
          crossorigin="anonymous"
    ></script>
  </%block>

</head>
<body class="ppss_auth">
${next.body()}
</body>

</html>