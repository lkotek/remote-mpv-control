<!DOCTYPE html>
<html lang="cs-cz">
<head>
    <meta charset='UTF-8' />
    <meta name="author" content="Lukas Kotek" /> 
    <meta content="initial-scale=1.0; maximum-scale=1.0; user-scalable=0;" name="viewport" />
    <meta name="mobile-web-app-capable" content="yes">
    <title>Media Remote Control</title>
    <link rel='stylesheet' href='/views/css/default.css' />     
</head>
<body>

<h1 id="top">Přehrává se:</h1>
<h2><em>{{playing}}</em></h2>

<table>
<tr>
  <td><a href="/volume/down">Zvuk &minus;</a></td>
  <td><a href="/volume/mute">Ztlumit</a></td>
  <td><a href="/volume/up">Zvuk &#43;</a></td>
</tr>
<tr>
  <td><a href="/playlist/prev">&nbsp;&lt;&lt;&nbsp;</a></td>
  <td><a href="/control/pause">&nbsp;|| &gt;&nbsp;</a></td>
  <td><a href="/playlist/next">&nbsp;&gt;&gt;&nbsp;</a></td>
</tr>
<tr>
  <td><a href="/window/screen">Okno</a></td>
  <td><a target="_blank" href="https://tv.seznam.cz/">Program</a></td>
  <td><a href="/window/aspect">Poměr</a></td>
</tr>
<tr>
  <td><a target="_blank" href="/playeroff">Zavřít</a></td>
  <td><a target="_blank" href="/sleep">Uspat</a></td>
  <td><a id="poweroff" onclick="return confirm('Určitě chcete centrum vypnout?')" href="/poweroff">Vypnout</a></td>
</tr>
</table>

<h1>Programy:</h1>

<ul>
  % for item in playlist:
    <li><a href="/play/{{item}}">{{playlist[item]}}</a></li>
  % end
</ul>

</body>

<div class="cntrl_items">
<a id="btn_full" href="#top">Jdi nahoru</a>
</div>

</html>
