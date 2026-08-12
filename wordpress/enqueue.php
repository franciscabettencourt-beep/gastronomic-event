<?php
/**
 * Gastronomy - September: carrega o CSS e o JS só nestas páginas.
 *
 * SÓ SERVE SE A PASTA gastronomic/ ESTIVER MESMO NO TEMA.
 *
 * Sem esse upload não há nada para carregar, e este ficheiro é o errado:
 * usa antes os dois snippets, wordpress/snippet-1-css.txt em CSS Snippet e
 * wordpress/snippet-2-js.txt em JavaScript Snippet. Ter os dois caminhos
 * ligados ao mesmo tempo carrega o estilo duas vezes.
 *
 * Cola no functions.php do tema, ou num plugin de snippets.
 * Ajusta a lista de slugs se mudares os endereços.
 */
add_action( 'wp_enqueue_scripts', function () {

    $slugs = array( 'gastronomic-september', 'setembro-gastronomico', 'septiembre-gastronomico', 'gastronomischer-september', 'septembre-gastronomique', 'atlantico', 'fogo', 'mediterraneo', 'algarve' );

    if ( ! is_page( $slugs ) ) {
        return;
    }

    $dir = get_stylesheet_directory() . '/gastronomic/assets';
    $uri = get_stylesheet_directory_uri() . '/gastronomic/assets';

    // Sem os ficheiros no sítio, filemtime() falha e o aviso do PHP sai
    // impresso no topo da página, à vista de quem visita. Já aconteceu.
    if ( ! file_exists( $dir . '/css/gastronomy-september.css' ) ) {
        return;
    }

    wp_enqueue_style(
        'gastronomy-september',
        $uri . '/css/gastronomy-september.css',
        array(),                                  // depois do main.min.css do tema
        filemtime( $dir . '/css/gastronomy-september.css' )
    );

    $js = $dir . '/js/carousel.js';
    if ( ! file_exists( $js ) ) {
        return;
    }

    wp_enqueue_script(
        'gastronomy-carousel',
        $uri . '/js/carousel.js',
        array(),
        filemtime( $js ),
        true
    );
}, 20 );
