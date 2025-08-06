let telaPrincipal = (document.currentScript.getAttribute('telaPrincipal') === 'telaPrincipal');
var query = document.querySelector.bind(document),
    queryAll = document.querySelectorAll.bind(document),
    queryId = document.getElementById.bind(document),
    queryName = document.getElementsByName.bind(document),
    servidor = "localhost:3000",
    empresa = "IPE.Transmissão",
    socket = io(servidor, { transports: ["polling", "websocket"] }),
    atual;

socket.on("connect", () => {
    socket.emit(empresa, "pegarDadosMensagem");
});

function updateClock() {
    fetch('hora.php')
        .then(response => response.json())
        .then(data => {
            document.getElementById('clock').textContent = data.hora;
        })
        .catch(error => console.error('Erro ao obter hora do servidor:', error));
}

const visibilidadeRelogio = () => {
    if (
        $('passagem').is(':hidden') &&
        $('louvor').is(':hidden')
    ) {
        $('#clock').fadeIn(200);
        updateClock();
        setInterval(updateClock, 1000);
    } else {
        $('#clock').fadeOut(200);
    }
};

socket.onAny((aplicativo, eventName, args) => {
    if (aplicativo === empresa) {
        if (eventName === "fecharJanela") {
            $(`body>*:visible`).fadeOut(200, function () {
                $(`body>*:visible>*`).html('');
                visibilidadeRelogio();
            });
        } else if (eventName === "fecharBiblia") {
            visibilidadeRelogio();
            if (atual === 'Mensagem') {
                if ($(`mensagem>rodape`).html(mensagem.corpo).css('display') !== 'none') $(`mensagem>rodape`).fadeOut(200);
            } else {
                $(`body>*:visible`).fadeOut(200, function () {
                    // this.querySelectorAll("*").forEach(obj => obj.innerhtml = "");
                    $(`body>*:visible>*`).html('');
                    visibilidadeRelogio();
                });
            }
        } else if (eventName === "Alerta") {
            if (telaPrincipal) {
                if (!$('body').hasClass('modal-open')) {
                    var dialog = bootbox.dialog({
                        message: args,
                        centerVertical: true,
                        closeButton: false,
                        className: 'bg-danger text-dark text-center',
                        onShow: function () {
                            $('body').addClass('modal-open');
                            setTimeout(function () {
                                dialog.modal('hide');
                            }, 5000);
                        },
                        onHidden: function () {
                            $('body').removeClass('modal-open');
                        }
                    });
                }
            }
        } else if (eventName === "obsSceneChanged") {
            atual = args;
            $(`body>*:visible`).fadeOut(200, function () {
                // this.querySelectorAll("*").forEach(obj => obj.innerhtml = "");
                $(`body>*:visible>*`).html('');
                visibilidadeRelogio();
            });            
        } else if (eventName === "pegarDadosMensagem") {
        } else if (eventName === "dadosMensagem") {
            $('mensagem>titulo').html(args.titulo);
            $('mensagem>corpo').html("");
            $('mensagem>corpo').append(`<ol></ol>`);
            args.topicos.forEach((topico, indice) => {
                $('mensagem>corpo>ol').append(`<li>${topico}</li>`);
                if (indice + 1 === args.topicos.length) $('mensagem>corpo>ol>li').fadeOut();
            });
        } else {
            mensagem(args);
        }
    }
});
// ----------------------------------------------------------------------------------
const inicio = () => {
    // if (typeof window.obsstudio != "undefined") {

    //     window.addEventListener('obsSceneChanged', function (event) {
    //         socket.emit(empresa, 'obsSceneChanged', event.detail.name);
    //     })

    // };
    setInterval(visibilidadeRelogio, 2000);

    if (/android|ipad|iphone|ipod/i.test(navigator.userAgent.toLowerCase())) $('body>*:not(#mensagem)').addClass('scrollJC');
}
// ----------------------------------------------------------------------------------
function mensagem(mensagem) {
    if (mensagem.tipo.includes("hino") || mensagem.tipo.includes("louvor")) tipo = "louvor"
    else tipo = mensagem.tipo;

    if ((atual === 'Mensagem') && (tipo === 'passagem')) {
        tipo = 'mensagem';
        mensagem.corpo = mensagem.titulo + '.' + mensagem.corpo;
        mensagem.titulo = 'passagem';
    }

    if ((tipo === 'louvor') || (tipo === 'passagem')) {
        mensagem.corpo = decodeURI(mensagem.corpo);

        new Promise((resolve) => {
            if ($(`body>${tipo}>titulo`).html() !== mensagem.titulo) {
                $(`body>${tipo}`).fadeOut(200, () => resolve(true));
            } else resolve(false);
        }).then((fechou) => {
            return new Promise((resolve) => {
                if ($(`body>${tipo}>corpo`).html() !== mensagem.corpo) $(`body>${tipo}>corpo`).fadeOut(200, () => resolve(true))
                else resolve(false);
            })
        }).then((ok) => {
            $(`body>*:not(${tipo})`).fadeOut(200, function () {
                $(`body>${tipo}>titulo`).html(mensagem.titulo);
                $(`body>${tipo}>corpo`).html(mensagem.corpo);
                $(`body>${tipo}>corpo`).fadeIn(200);
                $(`body>${tipo}`).fadeIn(200, visibilidadeRelogio);
            });
        });
    } else if (tipo === 'mensagem') {
        if ($(`mensagem`).css('display') === 'none') {
            $(`body>*:not(mensagem)`).fadeOut(200, function () {
                $(`mensagem`).fadeIn(200, visibilidadeRelogio);
            });
        }
        if (mensagem.titulo === 'topico') {
            if (mensagem.status === true) {
                $(`mensagem>corpo>ol>li:eq(${mensagem.indice})`).fadeIn(200);
            } else {
                $(`mensagem>corpo>ol>li:eq(${mensagem.indice})`).fadeOut(200);
            }
        } else if (mensagem.titulo === 'passagem') {
            mensagem.corpo = decodeURI(mensagem.corpo);
            if ($(`mensagem>rodape`).html(mensagem.corpo).css('display') === 'none') $(`mensagem>rodape`).fadeIn(200, visibilidadeRelogio);
        } else if (mensagem.titulo === 'limpaPassagem') {
            if ($(`mensagem>rodape`).html(mensagem.corpo).css('display') !== 'none') $(`mensagem>rodape`).fadeOut(200, visibilidadeRelogio);
        }
    }


    function ajustarFonteElemento(elemento, tamanhoOriginal) {
    const minFont = 10;
    let fontSize = tamanhoOriginal;

    elemento.style.fontSize = fontSize + "px";

    // Verifica se o conteúdo ultrapassa a tela
    const precisaReduzir = () => (
        elemento.scrollHeight > window.innerHeight || elemento.scrollWidth > window.innerWidth
    );

    while (precisaReduzir() && fontSize > minFont) {
        fontSize--;
        elemento.style.fontSize = fontSize + "px";
    }
}

function ajustarTodos() {
    const elementos = document.querySelectorAll('mensagem, passagem, louvor');

    elementos.forEach(tag => {
        if ($(tag).is(':visible')) {
            const filhos = tag.querySelectorAll('titulo, corpo, rodape');

            filhos.forEach(el => {
                const estilo = getComputedStyle(el);
                const tamanhoOriginal = parseFloat(estilo.fontSize);
                ajustarFonteElemento(el, tamanhoOriginal);
            });
        }
    });
}

window.addEventListener('load', ajustarTodos);
window.addEventListener('resize', ajustarTodos);

};