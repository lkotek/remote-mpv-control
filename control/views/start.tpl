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

<%
  iptv_selection = "mode_selection" if mode == "iptv" else ""
  video_selection = "mode_selection" if mode == "video" else ""
  audio_selection = "mode_selection" if mode == "audio" else ""
%>

<h1 id="top">Přehrává se:</h1>
<h2 class="selected_media"><em>{{playing}}</em></h2>

<table>
<tr>
  <td><a href="/volume/down">Zvuk &minus;</a></td>
  <td><a href="/volume/mute">Ztlumit</a></td>
  <td><a href="/volume/up">Zvuk &#43;</a></td>
</tr>
% if mode == "iptv":
<tr>
  <td><a href="/playlist/prev">&nbsp;&lt;&lt;&nbsp;</a></td>
  <td><a href="/control/pause">&nbsp;|| &gt;&nbsp;</a></td>
  <td><a href="/playlist/next">&nbsp;&gt;&gt;&nbsp;</a></td>
</tr>
% else:
<tr>
  <td><a href="/seek/backward">- 15 s</a></td>
  <td><a href="/control/pause">&nbsp;|| &gt;&nbsp;</a></td>
  <td><a href="/seek/forward">+ 15 s</a></td>
</tr>
% end
% if mode == "video":
<tr>
  <td><a href="/subtitle/forward">- 100</a></td>
  <td><strong>titulky</strong></td>
  <td><a href="/subtitle/backward">+ 100</a></td>
</tr>
% end
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
<tr>
  <td><a class="{{iptv_selection}}" href="/mode/iptv">IPTV</a></td>
  <td><a class="{{video_selection}}" href="/mode/video">Videa</a></td>
  <td><a class="{{audio_selection}}" href="#<!-- /mode/audio -->">Audio</a></td>
</tr>
</table>

% if mode == "iptv":
<h1>Programy:</h1>
<ul>
  % for item in player.playlist:
    <li><a href="/play/{{item}}">{{player.playlist[item]}}</a></li>
  % end
</ul>
% end
% if mode == "video":
<h1>Vybrat složku:</h1>
<ul>
  % for item in sorted(player.video_dirs, reverse=True):
    <li><a href="/select_dir/{{item}}">{{! player.video_dirs[item][1]}}</a></li>
  % end
</ul>
<h1 id="videos">Videa:</h1>
<ul>
  % for item in sorted(player.videos, reverse=True):
    <li><a href="/select_video/{{item}}">{{! player.videos[item][1]}}</a></li>
  % end
</ul>
<h1 id="selection">Výběr:</h1>
% end

% if player.video:
<h2 class="selected_media">Vybráno video: <em>{{player.video[1]}}</em></h2>
% else:
  <h2 class="selected_media">Video nevybráno.</h2>
% end

% if player.subtitle:
  <h2 class="selected_media">Vybrány titulky: <em>{{player.subtitle[1]}}</em></h2>
% else:
  <h2 class="selected_media">Titulky nevybrány.</h2>
% end

% if player.video:
<table>
<tr>
  <td><a href="/play_video">Přehrát</a></td>
  <td><a href="/select_reset">Resetovat</a></td>
</tr>
</table>
<h1>Titulky:</h1>
<ul>
  % for item in sorted(player.subtitles):
    <li><a href="/select_subtitle/{{item}}">{{! player.subtitles[item][1]}}</a></li>
  % end
</ul>
% end

% if mode == "audio":
<h1>Skladby:</h1>
% end

</body>

<table>
<tr>
  <td><a id="btn_full" href="#top">Jdi nahoru</a></td>
</tr>
</table>
</html>
