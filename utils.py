from datetime import datetime, date
from dateutil.relativedelta import relativedelta

def calcular_parcelas(data_inicio, data_referencia, data_desligamento=None):
    """
    Calcula o número da parcela com base na data de início e referência.
    Lógica: Início 02/02/2025 -> Ref Fev = Parcela 1 (Paga em Março).
    """
    if not data_inicio or not data_referencia:
        return 0, 0

    # Ensure dates
    if isinstance(data_inicio, str):
        data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
    if isinstance(data_referencia, str):
        # Reference is usually YYYY-MM. Treat as day 1 of month
        data_referencia = datetime.strptime(data_referencia + '-01', '%Y-%m-%d').date()
    
    # If desligado reference month >= shutdown month -> No Parcel? 
    # Prompt: "não recebe a parcela 02/02/2027, pois é o mes de dsligamento"
    # Implies if Reference Month == Month of Desligamento, Count is 0?
    # Or implies payment is for PREVIOUS month? 
    # "Paga primeira parcela no início de março" (referente a fevereiro).
    # Se desliga em Fev 2027, recebe início de Março (ref Fev)?
    # Usually affirmative. But prompt says: "não recebe parcela 02/02/2027" (date 2027-02-02).
    # Let's assume: If Month(Reference) >= Month(Desligamento), then 0.
    
    if data_desligamento:
        if isinstance(data_desligamento, str):
            data_desligamento = datetime.strptime(data_desligamento, '%Y-%m-%d').date()
        
        # Check if reference is AFTER or EQUAL to shutdown month
        # Logic: If I shutdown on Feb 5th, do I get Feb scholarship? Usually Pro-rata or Yes.
        # User says: "não recebe a parcela 02/02/2027" (start date 02/02/2025, prevision 01/01/2027... wait)
        # "mestrado início 02/02/2025, bolsita 05/05/2025 precisão 01/01/2027 ele é cadatado em fevereiro mas recebe aprimeira parcela no início de marlo e não recebe a parcela 02/02/2027"
        # 02/02/2027 is 2 years later.
        pass

    # Calculation
    # Diff in months
    diff = (data_referencia.year - data_inicio.year) * 12 + (data_referencia.month - data_inicio.month) + 1
    
    if diff <= 0:
        return 0 # Not started yet

    return diff
