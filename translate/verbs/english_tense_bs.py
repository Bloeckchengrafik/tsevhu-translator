raw_table = """
arise 	arose 	arisen
awake 	awoke 	awoken
be 	was 	been
be 	were 	been
bear 	bore 	borne
beat 	beat 	beaten
become 	became 	become
begin 	began 	begun
bend 	bent 	bent
bet 	bet 	bet
bind 	bound 	bound
bid 	bid 	bid
bite 	bit 	bitten
bleed 	bled 	bled
blow 	blew 	blown
break 	broke 	broken
breed 	bred 	bred
bring 	brought 	brought
broadcast 	broadcast 	broadcast
build 	built 	built
burst 	burst 	burst
buy 	bought 	bought
cast 	cast 	cast
catch 	caught 	caught
choose 	chose 	chosen
cling 	clung 	clung
come 	came 	come
cost 	cost 	cost
creep 	crept 	crept
cut 	cut 	cut
deal 	dealt 	dealt
dig 	dug 	dug
dive 	dove 	dived
do 	did 	done
draw 	drew 	drawn
dream 	dreamed dreamed
drink 	drank 	drunk
drive 	drove 	driven
eat 	ate 	eaten
fall 	fell 	fallen
feed 	fed 	fed
feel 	felt 	felt
fight 	fought 	fought
find 	found 	found
flee 	fled 	fled
fling 	flung 	flung
fly 	flew 	flown
forbid 	forbade 	forbidden
forget 	forgot 	forgotten
forgive 	forgave 	forgiven
freeze 	froze 	frozen
get 	got 	got
give 	gave 	given
go 	went 	gone
grind 	ground 	ground
grow 	grew 	grown
hang 	hung    hung
have 	had 	had
hear 	heard 	heard
hide 	hid 	hidden
hit 	hit 	hit
hold 	held 	held
hurt 	hurt 	hurt
keep 	kept 	kept
kneel 	knelt 	knelt
know 	knew 	known
lay 	laid 	laid
lead 	led 	led
leave 	left 	left
lend 	lent 	lent
let 	let 	let
lie	lay lain
light 	lit lit
lose 	lost 	lost
make 	made 	made
mean 	meant 	meant
meet 	met 	met
mistake 	mistook 	mistaken
mow 	mowed 	mown
overtake 	overtook 	overtaken
pay 	paid 	paid
proofread 	proofread 	proofread
put 	put 	put
quit 	quit 	quit
read 	read 	read
reset 	reset 	reset
ride 	rode 	ridden
ring 	rang 	rung
rise 	rose 	risen
run 	ran 	run
say 	said 	said
see 	saw 	seen
seek 	sought 	sought
sell 	sold 	sold
send 	sent 	sent
set 	set 	set
sew 	sewed 	sewn/sewed
shake 	shook 	shaken
shave 	shaved 	shaven
shed 	shed 	shed
shine 	shone 	shone
shoot 	shot 	shot
show 	showed 	shown
shrink 	shrank 	shrunk
shut 	shut 	shut
sing 	sang 	sung
sink 	sank 	sunk
sit 	sat 	sat
slay 	slew 	slain
sleep 	slept 	slept
slide 	slid 	slid
sling 	slung 	slung
sneak 	snuck   snuck
sow 	sowed 	sown/sowed
speak 	spoke 	spoken
speed 	sped 	sped
spend 	spent 	spent
spill 	spilt 	spilt
spin 	spun 	spun
spit 	spat 	spat
split 	split 	split
spread 	spread 	spread
spring 	sprang 	sprung
stand 	stood 	stood
steal 	stole 	stolen
stick 	stuck 	stuck
sting 	stung 	stung
stink 	stank 	stunk
strike 	struck 	struck
string 	strung 	strung
strive 	strove 	striven
swear 	swore 	sworn
sweep 	swept 	swept
swell 	swelled 	swollen
swim 	swam 	swum
swing 	swung 	swung
take 	took 	taken
teach 	taught 	taught
tear 	tore 	torn
think 	thought 	thought
throw 	threw 	thrown
thrust 	thrust 	thrust
tread 	trod 	trodden
understand 	understood 	understood
upset 	upset 	upset
wake 	woke 	woken
wear 	wore 	worn
weave 	wove 	worn
weave 	wove 	woven
weep 	wept 	wept
wet 	wet 	wet
win 	won 	won
wind 	wound 	wound
wring 	wrung 	wrung
write 	wrote 	written
"""

table = {}


def build_table():
    for line in raw_table.strip().split('\n'):
        present, past, past_participle = line.split()
        table[present] = (past, past_participle)


def get_past_irreg(present):
    return table[present][0]


def get_past_participle_irreg(present):
    return table[present][1]


def base_by_participle_irreg(past_participle):
    for base, (past, pp) in table.items():
        if pp == past_participle:
            return base


def is_irregular_participle(past_participle):
    return base_by_participle_irreg(past_participle) is not None


def base_by_past_irreg(past):
    for base, (p, pp) in table.items():
        if p == past:
            return base


def base_by_pariciple(past_participle):
    irreg = base_by_participle_irreg(past_participle)
    if irreg:
        return irreg

    return past_participle[:-2]


build_table()
