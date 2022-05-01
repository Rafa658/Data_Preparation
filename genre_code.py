def genre_code(genres):

    options = ["Action",
	"Adventure",
	"Animation",
	"Children's",
	"Comedy",
	"Crime",
	"Documentary",
	"Drama",
	"Fantasy",
	"Film-Noir",
	"Horror",
	"Musical",
	"Mystery",
	"Romance",
	"Sci-Fi",
	"Thriller",
	"War",
	"Western"]

    acc = 0 # acumulador
    for genre in genres:
        if genre not in options:
            acc+=0
        else:
            acc+=2**options.index(genre)
        
    return acc