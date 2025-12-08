from django.db import models

class OperationalSettings(models.Model):
    # Configurações Gerais e Branding
    company_name = models.CharField(max_length=255, verbose_name="Nome da Empresa", default="SistemasBr")
    company_logo = models.ImageField(upload_to='logos/', blank=True, null=True, verbose_name="Logo da Empresa", help_text="Logo que aparecerá no cabeçalho.")
    favicon = models.ImageField(upload_to='logos/', blank=True, null=True, verbose_name="Favicon", help_text="Ícone que aparece na aba do navegador.")
    footer_text = models.CharField(max_length=255, blank=True, verbose_name="Texto do Rodapé", help_text="Ex: © 2024 Nome da Empresa. Todos os direitos reservados.")

    # Contato e Links Legais
    contact_email = models.EmailField(blank=True, verbose_name="E-mail de Contato Público")
    privacy_policy_url = models.URLField(blank=True, verbose_name="URL da Política de Privacidade")
    terms_of_service_url = models.URLField(blank=True, verbose_name="URL dos Termos de Serviço")

    # Funcionalidades
    enable_public_registration = models.BooleanField(default=False, verbose_name="Habilitar Cadastro Público", help_text="Permite que novos usuários se cadastrem no sistema.")
    enable_feedback_system = models.BooleanField(default=True, verbose_name="Habilitar Sistema de Feedback", help_text="Permite que usuários enviem feedback nos artigos.")

    # Integrações
    google_analytics_id = models.CharField(max_length=50, blank=True, verbose_name="ID do Google Analytics", help_text="Ex: UA-12345678-1")

    # Configurações de E-mail
    sender_email = models.EmailField(verbose_name="E-mail Remetente Padrão", help_text="O e-mail que será usado como remetente para comunicações do sistema.")
    email_host = models.CharField(max_length=255, verbose_name="Servidor SMTP (Host)", blank=True)
    email_port = models.PositiveIntegerField(verbose_name="Porta SMTP", default=587, blank=True)
    email_host_user = models.CharField(max_length=255, verbose_name="Usuário SMTP", blank=True)
    email_host_password = models.CharField(max_length=255, verbose_name="Senha SMTP", blank=True)
    email_use_tls = models.BooleanField(default=True, verbose_name="Usar TLS")
    email_use_ssl = models.BooleanField(default=False, verbose_name="Usar SSL")

    class Meta:
        verbose_name = "Configuração Operacional"
        verbose_name_plural = "Configurações Operacionais"

    def __str__(self):
        return "Configurações Operacionais"
