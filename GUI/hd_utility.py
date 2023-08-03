
import qrcode # Install using: pip install qrcode[pil]
from PIL import ImageTk, Image
import json
from reportlab.pdfgen import canvas # pip install reportlab pillow

from reportlab.lib.pagesizes import A4  # Import A4 constant
from PIL import Image

from reportlab.platypus import PageBreak
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Image as PlatypusImage, PageBreak, Spacer


class HD_Utility:
    # =================================================================== #
    def make_qr(data: str, file_name: str) -> None:
        """
        Generate a QR code image and save it to a file.

        Parameters:
        data (str): The information to be encoded into the QR code.
        file_name (str): The name of the file where the QR code will be saved.

        Returns:
        None

        Example Usage:
        make_qr("https://www.openai.com", "openai_qr.png")

        Requirement:
        import qrcode # Install using: pip install qrcode[pil]
        """

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill='black', back_color='white')
        img.save(file_name)
        return img


    # =================================================================== #
    import json
    def read_json_file(file_path):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return {}
        except json.JSONDecodeError:
            print(f"Error decoding JSON data in file: {file_path}")
            return {}


    # =================================================================== #
    # from PIL import ImageTk, Image
    def convert_to_pil(label):
        # Get the PhotoImage object from the label
        photo_image = label.cget("image")

        # Convert the PhotoImage to a PIL Image object
        pil_image = ImageTk.getimage(photo_image)

        return pil_image

    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4  # Import A4 constant
    from PIL import Image

    def create_pdf_deprecated(images, texts, output_filename):
        # Install: pip install reportlab pillow

        # Open a New PDF File
        c = canvas.Canvas(output_filename, pagesize=A4)  # Use A4 size
        page_width, page_height = A4

        # Get Image(s) Size
        image_height= images[0].height
        image_width= images[0].width

        # Set Initial Coordinates
        x_coord = page_width/2 - image_width/2
        constant_decrease = 50
        y_coord = page_height - image_height - constant_decrease

        # Add images
        for image in images:
            c.drawInlineImage(image, x_coord, y_coord)  # You may need to adjust coordinates
            y_coord -= (constant_decrease + image_height)

        # Next Page
        c.showPage()

        # Set Text Coordinate
        y_coord = page_height - constant_decrease

        # Add descriptions
        for text in texts:
            c.drawString(x_coord, y_coord, text)
            y_coord -= constant_decrease*2

        # Close the PDF
        c.save()

    def create_pdf(images_paths, texts, output_filename):

        '''
        Example:
        txts = ("This is a description hgasdfhAGFH,DGSFHDSagf hkHJLDHASFG HJaglfkghdfhGJ KHJasdgfhkDGALSFdsfgazdgsdfgasgasfgasfgsgasgasfdgsdfgasdfgasdfgasHGdsf HJKDFGHkadgfhdklsfgjhfg 1",
        "This is a description hgasdfhAGFH,DGSFHDSagf hkHJLDHASFG HJaglfkghdfhGJ KHJasdgfhkDGALSFHGdsf HJKDFGHkadgfhdklsfgjhfg 2")
        output_filename = "output.pdf"
        hd_utility.HD_Utility.create_pdf(images_paths = ('1.jpg', 'image_1.png'), texts = txts, output_filename= output_filename)
        '''

        # Create a SimpleDocTemplate, which represents a PDF document
        doc = SimpleDocTemplate(output_filename, pagesize=A4)

        # Create a list to hold the elements to be added to the document
        elements = []

        # Get the width and height of the A4 size
        width, height = A4

        # Add image1 at the top of the page
        for img in images_paths:
            elements.append(PlatypusImage(img, width=2*width/3, height=height/3))  # Adjust the width and height as needed
            elements.append(Spacer(width, height/10))

        # First, get a style to use for the Paragraph
        styles = getSampleStyleSheet()
        style = styles["BodyText"]

        # Create the Paragraph with the text and style, and add it to the elements
        for text in texts:
            p = Paragraph(text, style)
            elements.append(p)

        # Build the PDF
        doc.build(elements)