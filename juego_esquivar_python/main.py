import pygame #librerías necesarias
import time
import random
pygame.font.init() #inicializa el módulo de fuentes de letra


WIDTH, HEIGHT = 800, 600  #ajustes de ventana
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Juego Erick")

BG = pygame.transform.scale(pygame.image.load("img/spacebg.jpg"), (WIDTH, HEIGHT)) #importar fondo
#también escala la imagen de forma que ocupe la pantalla

PLAYER_WIDTH = 40
#ancho y largo del jugador
PLAYER_HEIGHT = 60

PLAYER_VEL = 5 #velocidad del jugador

STAR_WIDTH = 10 
#medidas de los proyectiles
STAR_HEIGHT = 20

STAR_VEL = 3 #velocidad de las estrellas

FONT = pygame.font.SysFont("comicsans", 25) #fuente de letra y tamaño

def draw(player, elapsed_time, stars):
    WIN.blit(BG, (0, 0)) #dibuja el fondo y las coordenadas; 0,0 es la esquina supererior izquierda

    time_text = FONT.render(f"Tiempo: {round(elapsed_time)}s", 1, "white")
    #primero le pasamos el texto a renderizar, la f permite mostrar una variable dentro del texto
    #round redondea un número, el 1 se asegura de que el texto luzca mejor y el color

    WIN.blit(time_text, (10, 10)) #dibuja el texto y lo pone arriba

    pygame.draw.rect(WIN, (255, 0, 0), player)
    #dibuja el rectángulo con los datos que le dimos, el primero es la ventana y el otro es el color RGB

    for star in stars:
        pygame.draw.rect(WIN, "white", star) #dibuja cada proyectil

    pygame.display.update() #refresca la pantalla, aplica cualquier cambio de "dibujo" en la pantalla

def main():
    run = True

    player = pygame.Rect(400, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    #primero las coordenadas en las cuales va a aparecer, luego el ancho y alto del rectángulo que será
    #el jugador

    clock = pygame.time.Clock() #objeto reloj para controlar la velocidad del movimiento

    start_time = time.time() #sirve como cronómetro cuando inicie el juego

    elapsed_time = 0

    star_add_increment = 2000 #se irán agregando proyectiles cada 2000 milisegundos (2 segundos)
    star_count = 0 #dice cuándo se debería agregar el siguiente proyectil

    stars = [] #almacena los proyectiles que hay en la pantalla para dibujarlos

    hit = False

    while run:

        #clock.tick(60) #max de fps o número de veces que se desea que el loop corra por segundo

        star_count += clock.tick(60) #devuelve el número de milisegundos desde el último tic

        elapsed_time = time.time() - start_time #para guardar el tiempo que llevamos en segundos


        if star_count > star_add_increment:
        #como empieza en 0, cuando pase los 2000 se agregará un proyectil
            for _ in range(3): #agregar tres proyectiles, la variable puede ser cualquiera
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                #elige un número random entre 0 y el ancho de la pantalla
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                #posición en x que aparece generado al azar, se usar la y negativa para que parezca
                #que aparece desde antes de la pantalla y que no se vea cómo aparece, lo demás son las
                #medidas de los proyectiles
                stars.append(star) #agrega la estrella generada a la lista

            star_add_increment = max(200, star_add_increment - 50)
            #va disminuyendo el valor entonces las estrellas aparecen más rápido, menor de 200 no puede
            #ser
            star_count = 0
            #otra vez vuelve a ser cero para que se repita el la condición en el siguiente ciclo


        for event in pygame.event.get(): #revisa cada evento que pasa, si le da en cerrar pues se cierra
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed() #lector y configuración de movimiento
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0: #si es negativo no lo deje mover
            player.x -= PLAYER_VEL

        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH: #igual a lo de arriba
            player.x += PLAYER_VEL

        for star in stars[:]: #acá se hace una copia de la lista
        #se hace porque se irán removiendo las estrellas que toquen la parte baja de la pantalla o que
        #toquen el jugador
            star.y += STAR_VEL
            if star.y > HEIGHT:
            #checa si ya pasó la pantalla
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
            #checa si se estella con el jugador
                stars.remove(star)
                hit = True #el proyectil le dio al jugador
                break
        
        if hit:
            lost_text = FONT.render("Perdiste", 1, "white") #para mostrar el texto si se pierde
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2))
            #cálculos para poner el texto en el centro
            pygame.display.update()
            pygame.time.delay(4000) #esperar 5 segundos
            break
        
        draw(player, elapsed_time, stars) #por cada frame llamamos la función para que siga dibujando en la
        #ventana, junto con el tiempo transcurrido y los proyectiles

    pygame.quit() #para asegurarse de cerrar el juego correctamente

if __name__ == "__main__":
    main()