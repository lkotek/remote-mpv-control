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

<div class="cntrl_items">
<a id="btn01" class="control" href="/volume/down">Zvuk &minus;</a>
<a id="btn02" class="control" href="/volume/mute">Ztlumit</a>
<a id="btn03" class="control" href="/volume/up">Zvuk &#43;</a>
</div>

<div class="cntrl_items">
<a id="btn04" class="control" href="/window/screen">Okno</a>
<a id="btn05" class="control" href="/playlist/prev">&nbsp;&lt;&lt;&nbsp;</a>
<a id="btn06" class="control" href="/control/pause">&nbsp;|| &gt;&nbsp;</a>
<a id="btn07" class="control" href="/playlist/next">&nbsp;&gt;&gt;&nbsp;</a>
</div>

<div class="cntrl_items">
<a id="btn08" target="_blank" class="control" href="https://tv.seznam.cz/">TV Program</a>
<a id="btn09" class="control" onclick="return confirm('Určitě chcete centrum vypnout?')" href="/poweroff">Vypnout</a>
</div>

<div class="cntrl_items">
<a id="btn10" target="_blank" class="control" href="/playeroff">Zavřít</a>
<a id="btn11" target="_blank" class="control" href="/sleep">Uspat</a>
</div>

<h1>Programy:</h1>

<ul>
  % for item in playlist:
    <li><a href="/play/{{item}}">{{playlist[item]}}</a></li>
  % end
</ul>

</body>

<div class="cntrl_items">
<a class="control" href="#top">Jdi nahoru</a>
</div>

</html>
