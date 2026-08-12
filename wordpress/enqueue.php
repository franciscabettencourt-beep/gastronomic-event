<?php
/**
 * Gastronomy - September: carrega o CSS e o JS só nestas páginas.
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

    wp_enqueue_style(
        'gastronomy-september',
        $uri . '/css/gastronomy-september.css',
        array(),                                  // depois do main.min.css do tema
        filemtime( $dir . '/css/gastronomy-september.css' )
    );

    wp_enqueue_script(
        'gastronomy-carousel',
        $uri . '/js/carousel.js',
        array(),
        filemtime( $dir . '/js/carousel.js' ),
        true
    );
}, 20 );
