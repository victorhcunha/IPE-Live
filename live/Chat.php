<?php
$channelId = "UCIjAWGccTvvw9QW0r_6ZY4A";
$liveUrl = "https://www.youtube.com/channel/{$channelId}/live";

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $liveUrl);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
$html = curl_exec($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

if ($httpCode !== 200 || empty($html)) {
    echo "❌ Erro ao carregar a página da live.";
    exit;
}

if (preg_match('/"videoId":"(.*?)"/', $html, $matches)) {
    $videoId = $matches[1];
    $chatUrl = "https://www.youtube.com/live_chat?v={$videoId}&is_popout=1";
    // Redireciona para o chat na mesma janela
    header("Location: $chatUrl");
    exit;
} else {
    // Mostra mensagem e botão para recarregar a página
    echo '<p>⚠️ Nenhuma live ativa foi detectada no momento.</p>';
    echo '<button onclick="window.location.reload()">Tentar novamente</button>';
}
?>
