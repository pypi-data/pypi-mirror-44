<%inherit file="${context['logintpl']}" />

<form action="${request.route_url('ppsschangepassword')}" method="POST">
    
    <input type="password" name="oldpassword" placeholder="current password">
    <br/>
    <input type="password" name="newpassword" placeholder="new password">
    <br/>
    <input type="password" name="confirmnewpassword" placeholder="confirm new password">
    <br/>
    <input type="submit" name="submit" value="entra"/>

    <p>${msg}</p>
</form>