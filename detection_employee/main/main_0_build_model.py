########## BUILD MODEL BIN
import insightface_paddle_face as face


parser = face.parser()
args = parser.parse_args()
args.build_index = "./dataset/index.bin"
args.img_dir = "./dataset"
args.label = "./dataset/label.txt"
predictor = face.InsightFace(args)
predictor.build_index()