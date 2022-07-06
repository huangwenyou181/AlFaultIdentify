import click
from application import db, app
from application.models import Class, User

@app.cli.command()
@click.option('--drop', is_flag=True, help="Create after drop")
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    
    user = User(name="admin")
    user.set_password("admin")
    db.session.add(user)
    db.session.commit()
    
    click.echo("Database initialization done.")

@app.cli.command()
def addclass():
    classes = [
        {"classname": "Alstroemeria",
        "classtext": "六出花（学名：Alstroemeria aurea Graham）是六出花科、六出花属植物。多年生宿根草本，高约1米，根肥厚肉质，平卧土中延长，须根多；茎自根茎上不定芽萌发，直立而细长，叶片多数，互生状散生，披针形，光滑。花序下为一轮生叶，总花梗5，各具花2-3朵，插生于花被片基部；子房下位，3室，具种子多数。"
        },
        {"classname": "Antirrhinum",
        "classtext": "金鱼草（学名：Antirrhinum majus L.）是车前科、金鱼草属植物。多年生直立草本，茎基部有时木质化，高可达80厘米。茎基部无毛，中上部被腺毛，基部有时分枝。叶下部的对生。总状花序顶生，密被腺毛；花梗长5-7毫米；花萼与花梗近等长，5深裂，裂片卵形，钝或急尖；雄蕊4枚，2强。"
        },
        {"classname": "Campanula",
        "classtext": "风铃草（学名：Campanula medium L.）是桔梗科、风铃草属二年生宿根草本植物，株高50-120厘米；茎粗壮直立，基生。叶簇生，卵形至倒卵形；小花1-2朵聚生成总状花序，花冠钟形，长约6厘米，有白、蓝或紫等色；蒴果，带有宿存的花萼裂片；种子多数，椭圆状，平滑。"
        },
        {"classname": "daisy",
        "classtext": "雏菊（学名：Bellis perennis L.），又名马兰头花、延命菊，春菊、太阳菊等。是菊科雏菊属植物的一种，多年生草本植物。高10厘米左右。雏菊原产于欧洲。原种被视为丛生的杂草，开花期在春季。雏菊在能够渡夏的寒冷地区可以进行分枝繁殖。"
        },
        {"classname": "dandelion",
        "classtext": "蒲公英（拉丁学名：Taraxacum mongolicum Hand.-Mazz.）菊科，蒲公英属多年生草本植物。根圆锥状，表面棕褐色，皱缩，叶边缘有时具波状齿或羽状深裂，基部渐狭成叶柄，叶柄及主脉常带红紫色，花葶上部紫红色，密被蛛丝状白色长柔毛；头状花序，总苞钟状，瘦果暗褐色，长冠毛白色，花果期4～10月。"
        },
        {"classname": "Dianthus",
        "classtext": "康乃馨（学名：Dianthus）：是石竹科、石竹属多年生草本植物，是多种石竹属园艺品种的通称。为多年生草本植物，株高70-100厘米，基部半木质化。整个植株被有白粉，呈灰绿色。茎干硬而脆，节膨大。"
        },
        {"classname": "Dianthus_chinensis",
        "classtext": "石竹，为双子叶植物纲、石竹科、石竹属多年生草本，高30-50厘米，全株无毛，带粉绿色。茎由根颈生出，疏丛生，直立，上部分枝。叶片线状披针形，顶端渐尖，基部稍狭，全缘或有细小齿，中脉较显。"
        },
        {"classname": "Digitalis_purpurea",
        "classtext": "毛地黄（学名：Digitalis purpurea L）是玄参科、毛地黄属一年生或多年生草本植物。除花冠外，全体被灰白色短柔毛和腺毛，有时茎上几无毛，高60-120厘米。茎单生或数条成丛。茎直立，少分枝，全株被灰白色短柔毛和腺毛。"
        },
        {"classname": "Echinacea",
        "classtext": "紫松果菊属(Echinacea)开紫花，多年生，常栽作沿边植物(尤其是狭叶紫松果菊〔E. angustifolia〕和紫松果菊〔E. purpurea〕)；其根黑色，气味浓烈，茎有毛，叶基生，具长柄。"
        },
        {"classname": "Eschscholtzia",
        "classtext": "花菱草，（学名：Eschscholtzia californica Cham.），为罂粟科多年生草本植物，常作一、二年生栽培。耐寒力较强，喜冷凉干燥气候、不耐湿热，炎热的夏季处于半休眠状态，常枯死 ，秋后再萌发。原产美国加利福尼亚州。"
        },
        {"classname": "Fritillaria",
        "classtext": "贝母（学名：Fritillaria spp.）是百合科、贝母属多年生草本植物的统称。鳞茎深埋土中，外有鳞茎皮；茎直立，不分枝，一部分位于地下；基生叶有长柄；茎生叶对生、轮生或散生；花较大或略小，通常钟形，俯垂，辐射对称，单朵顶生或多朵排成总状花序或伞形花序；蒴果具6棱，棱上常有翅，室背开裂；种子多数，扁平，边缘有狭翅。"
        },
        {"classname": "Gardenia",
        "classtext": "栀子（学名：Gardenia jasminoides Ellis）别名：黄栀子、山栀、白蟾，是茜草科栀子属灌木，高0.3-3米；嫩枝常被短毛，枝圆柱形，灰色。叶对生，革质，稀为纸质，少为3枚轮生，叶形多样，两面常无毛，上面亮绿，下面色较暗。"
        },
        {"classname": "Gazania",
        "classtext": "勋章菊（学名：Gazania rigens Moench）是菊科，勋章菊属多年生草本植物，株高可达40厘米，叶由根际丛生，叶片披针形或倒卵状披针形，叶背密被白毛，叶形丰富。头状花序单生，舌状花和管状花两种，花色丰富多彩，有白、黄、橙红等色，花瓣有光泽，花心处多有黑色、褐色5-10月开花。"
        },
        {"classname": "Jasminum",
        "classtext": "茉莉花（学名： Jasminum sambac (L.) Aiton）是木犀科、素馨属直立或攀援灌木，高达3米。小枝圆柱形或稍压扁状，有时中空，疏被柔毛。叶对生，单叶，叶片纸质，圆形、椭圆形、卵状椭圆形或倒卵形，两端圆或钝，基部有时微心形，在上面稍凹入或凹起，下面凸起，细脉在两面常明显，微凸起，除下面脉腋间常具簇毛外，其余无毛。"
        },
        {"classname": "lancifolium",
        "classtext": "卷丹（学名：Lilium lancifolium Thunb.）：卷丹花瓣有平展的，有向外翻卷的，故有“卷丹”美名。鳞茎近宽球形，高约3.5厘米，直径4-8厘米；鳞片宽卵形，长2.5-3厘米，宽1.4-2.5厘米，白色。茎高0.8-1.5米，带紫色条纹，具白色绵毛。"
        },
        {"classname": "Lathyrus",
        "classtext": "山黧豆属（学名：Lathyrus L.）别名香豌豆属，属于豆科、蝶形花亚科、野豌豆族的一个属。 为一年生或多年生、草质藤本植物。 该属共有约130种，分布于北温带、热带非洲和南美的高山上。中国有18种，其中特有种有三，引进栽培者三。"
        },
        {"classname": "Lycoris_radiata",
        "classtext": "石蒜（拉丁学名：Lycoris radiata (L’Her.) Herb.）为石蒜科石蒜属植物。鳞茎近球形，直径1-3厘米。秋季出叶，叶狭带状，长约15厘米，宽约0.5厘米，顶端钝，深绿色，中间有粉绿色带。伞形花序有花4-7朵，花鲜红色。花期8-9月，果期10月。"
        },
        {"classname": "Matthiola",
        "classtext": "紫罗兰（学名：Matthiola incana (L.) R. Br.）是十字花科、紫罗兰属二年生或多年生草本。全株密被灰白色具柄的分枝柔毛。茎直立，多分枝，基部稍木质化。叶片长圆形至倒披针形或匙形。原产地中海沿岸。中国南部地区广泛栽培，欧洲名花之一。"
        },
        {"classname": "Narcissus",
        "classtext": "水仙（Narcissus tazetta L. var. chinensis Roem.）：又名中国水仙，是多花水仙的一个变种。是石蒜科多年生草本植物。水仙的叶由鳞茎顶端绿白色筒状鞘中抽出花茎（俗称箭）再由叶片中抽出。一般每个鳞茎可抽花茎1-2枝，多者可达8-11枝，伞状花序。花瓣多为6片，花瓣末处呈鹅黄色。"
        },
        {"classname": "Nymphaea",
        "classtext": "睡莲属（学名：Nymphaea L.）：根茎平生或直立；叶浮于水面，圆形或卵形，基部心形，有时稍盾状，背面常有颜色；花大而美丽，颜色种种，浮水或突出水面；萼片4；花瓣和雄蕊多数，着生于子房之近顶；心皮多数，藏于肉质的花托内，并愈合成一多室、半下位的子房，顶冠以放射状的花柱。"
        },
        {"classname": "peach_blossom",
        "classtext": "桃花，属蔷薇科植物。叶椭圆状披针形，核果近球形，主要分果桃和花桃两大类。桃花原产于中国中部、北部，现已在世界温带国家及地区广泛种植，其繁殖以嫁接为主。"
        },
        {"classname": "Pharbitis",
        "classtext": "牵牛子（英文名：SEMEN PHARBITIDIS.），别名：黑丑、白丑、二丑、喇叭花、姜姜籽，牵牛、朝颜花。为旋花科牵牛属，一年生蔓性缠绕草本花卉。蔓生茎细长，约3～4米，全株多密被短刚毛。叶互生，全缘或具叶裂。聚伞花序腋生，1朵至数朵。花冠喇叭样。花色鲜艳美丽。"
        },
        {"classname": "Pomegranate",
        "classtext": "石榴花，落叶灌木或小乔木石榴的花；为石榴属植物，石榴树干灰褐色，有片状剥落，嫩枝黄绿光滑，常呈四棱形，枝端多为刺状，无顶芽。石榴花单叶对生或簇生，矩圆形或倒卵形，新叶嫩绿或古铜色。"
        },
        {"classname": "Rhododendron",
        "classtext": "杜鹃（学名：Rhododendron simsii Planch.）：是双子叶植物纲、杜鹃花科、杜鹃属的常绿灌木、落叶灌木 [1]  。又名映山红、山石榴。相传，古有杜鹃鸟，日夜哀鸣而咯血，染红遍山的花朵，因而得名。杜鹃花一般春季开花，每簇花2-6朵，花冠漏斗形，有红、淡红、杏红、雪青、白色等，花色繁茂艳丽。"
        },
        {"classname": "Rosa",
        "classtext": "蔷薇（学名：Rosa sp.）：是蔷薇属部分植物的通称，主要指蔓藤蔷薇的变种及园艺品种。大多是一类藤状爬篱笆的小花，是原产于中国的落叶灌木，变异性强。茎刺较大且一般有钩，每节大致有3、4个；叶互生，奇数羽状复叶，小叶为5-9片，叶缘有齿，叶片平展但有柔毛。"
        },
        {"classname": "roses",
        "classtext": "玫瑰（学名：Rosa ssp. 英文名称：Rosa）：是蔷薇目，蔷薇科、蔷薇属多种植物和培育花卉的通称名字。直立、蔓延或攀援灌木，多数被有皮刺、针刺或刺毛，稀无刺，有毛、无毛或有腺毛。叶互生；花单生；花托球形、坛形至杯形；花瓣5，稀4，开展，覆瓦状排列，白色、黄色，粉红色至红色。"
        },
        {"classname": "Strelitzia",
        "classtext": "鹤望兰（Strelitzia reginae Aiton）芭蕉科鹤望兰亚科多年生草本植物，无茎。叶片长圆状披针形，长25-45cm，宽10cm。叶片顶端急尖；叶柄细长。花数朵生于总花梗上，下托一佛焰苞；佛焰苞绿色，边紫红，萼片橙黄色，花瓣暗蓝色"
        },
        {"classname": "sunflowers",
        "classtext": "向日葵（学名：Helianthus annuus）别名太阳花，是菊科向日葵属的植物。向日葵是一年生草本，高1~3米，茎直立，粗壮，圆形多棱角，被白色粗硬毛，性喜因花序随太阳转动而得名。向日葵花语为爱慕、光辉、高傲之意，仰慕、凝视着你。温暖，耐旱，能产果实葵花籽。"
        },
        {"classname": "Tropaeolum_majus",
        "classtext": "旱金莲（拉丁学名：Tropaeolum majus.）是双子叶植物纲旱金莲科旱金莲属植物，为多年生的半蔓生或倾卧植物。旱金莲株高30cm~70cm；基生叶具长柄，叶片五角形，三全裂，二回裂片有少数小裂片和锐齿；花单生或2朵~3朵成聚伞花序，花瓣五，萼片8枚~19枚，黄色，椭圆状倒卵形或倒卵形，花瓣与萼片等长，狭条形。"
        },
        {"classname": "tulips",
        "classtext": "郁金香（学名：Tulipa gesneriana L.）是百合科、郁金香属植物。叶3～5枚，条状披针形至卵状披针状，花单朵顶生，大型而艳丽，花被片红色或杂有白色和黄色，有时为白色或黄色，长5～7厘米，宽2～4厘米，6枚雄蕊等长，花丝无毛，无花柱，柱头增大呈鸡冠状，花期4～5月。"
        }
    ]
    for c in classes:
        cl = Class(classname=c["classname"],classtext=c["classtext"])
        db.session.add(cl)
    db.session.commit()
    click.echo("class added done.")


    
@app.cli.command()
@click.option('--username', prompt = True, help = "username to login")
@click.option('--password', prompt = True, confirmation_prompt=True, help = "password to login")
def userset(username, password):
    db.create_all()
    user = User.query.filter(User.name == username).first()
    if user is not None:
        click.echo("User already exists, now reset password")
        user.set_password(password)
    else:
        click.echo("creating user......")
        user = User(name=username)
        user.set_password(password)
        db.session.add(user)
    db.session.commit()
    click.echo("done.")
        