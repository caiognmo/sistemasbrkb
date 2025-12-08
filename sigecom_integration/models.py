from django.db import models
from tinymce.models import HTMLField
from bs4 import BeautifulSoup

def html_to_rtf_simplified(html):
    """
    Converte um conteúdo HTML simples para um formato RTF básico,
    extraindo o texto e preservando as quebras de parágrafo.
    A formatação (negrito, itálico, etc.) é removida.
    """
    if not html:
        return ""
    
    # Usa BeautifulSoup para extrair o texto do HTML
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text(separator="\\n") # Usa \n como separador para identificar parágrafos
    
    # Escapa caracteres especiais do RTF: '\', '{', '}'
    text = text.replace('\\', '\\\\').replace('{', '\\{').replace('}', '\\}')
    
    paragraphs = text.split('\\n')
    rtf_paragraphs = []
    
    # Envolve cada parágrafo na estrutura RTF especificada pelo usuário
    for p_text in paragraphs:
        p_text = p_text.strip()
        if p_text:
            # Estrutura de parágrafo RTF, escapando as barras invertidas para o Python
            rtf_paragraphs.append(f"{{{{\\\\pard \\\\ql \\\\f0 \\\\sa180 \\\\li0 \\\\fi0 {p_text}\\\\par}}}}")
    
    rtf_body = ' '.join(rtf_paragraphs)
    
    # Estrutura final do documento RTF, baseada no exemplo do usuário
    final_rtf = f"{{{{\\pard \\\\ql \\\\f0 \\\\sa180 \\\\li0 \\\\fi0 {rtf_body}\\\\par}}}}\\r\\n"
    
    return final_rtf

class Aviso(models.Model):
    TIPO_AVISO_CHOICES = [
        ('popup', 'Pop-up'),
        ('card', 'Card'),
    ]

    id = models.AutoField(primary_key=True)
    tipo_aviso = models.CharField(max_length=10, choices=TIPO_AVISO_CHOICES, default='janela')
    titulo = models.CharField(max_length=200)
    mensagem = HTMLField("Mensagem (Editor Visual)")
    mensagem_rtf = models.TextField(
        verbose_name="Mensagem em formato RTF",
        blank=True,
        editable=False,
        help_text="Conteúdo convertido para RTF, gerado automaticamente ao salvar."
    )
    link_botao = models.URLField(max_length=500, blank=True, help_text="URL para o botão (disponível apenas para 'Modo Janela').")
    texto_botao = models.CharField(max_length=100, blank=True, help_text="Texto do botão (disponível apenas para 'Modo Janela').")
    ativo = models.BooleanField(default=True, help_text="Marque esta opção para incluir o aviso na exportação JSON. Desmarque para ocultá-lo.")

    def __str__(self):
        return f"{self.id} - {self.titulo}"

    def save(self, *args, **kwargs):
        # Converte o HTML da 'mensagem' para RTF e salva em 'mensagem_rtf'
        self.mensagem_rtf = html_to_rtf_simplified(self.mensagem)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Aviso Sigecom"
        verbose_name_plural = "Avisos Sigecom"

    def get_export_id(self):
        return self.id
